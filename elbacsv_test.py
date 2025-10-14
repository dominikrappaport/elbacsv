import pytest
from elbacsv import parse_key_value_string, KEYS


class TestParseKeyValueString:
    """Test suite for the parse_key_value_string function."""

    def test_empty_string(self):
        """Test parsing an empty string."""
        result = parse_key_value_string("")
        assert isinstance(result, dict)
        assert all(result[k] == "" for k in KEYS)

    def test_single_key_value_pair(self):
        """Test parsing a string with a single key-value pair."""
        input_str = "Verwendungszweck: Test payment"
        result = parse_key_value_string(input_str)

        assert result["Verwendungszweck"] == "Test payment"
        # All other keys should be empty
        for key in KEYS:
            if key != "Verwendungszweck":
                assert result[key] == ""

    def test_multiple_key_value_pairs(self):
        """Test parsing a string with multiple key-value pairs."""
        input_str = "Verwendungszweck: Payment for services IBAN Empfänger: DE89370400440532013000 Empfänger: John Doe"
        result = parse_key_value_string(input_str)

        assert result["Verwendungszweck"] == "Payment for services"
        assert result["IBAN Empfänger"] == "DE89370400440532013000"
        assert result["Empfänger"] == "John Doe"

    def test_specific_key_value_pairs(self):
        """Test parsing a specific string with multiple key-value pairs."""
        input_str = "Auftraggeber: Mag. Christine Rappaport IBAN Auftraggeber: AT331100012026219100 BIC Auftraggeber: BKAUATWWXXX Urspr. Empfänger: Mag. Christine Rappaport"
        result = parse_key_value_string(input_str)

        assert result["Auftraggeber"] == "Mag. Christine Rappaport"
        assert result["IBAN Auftraggeber"] == "AT331100012026219100"
        assert result["BIC Auftraggeber"] == "BKAUATWWXXX"
        assert result["Urspr. Empfänger"] == "Mag. Christine Rappaport"

    def test_key_with_empty_value(self):
        """Test parsing when a key has an empty value."""
        input_str = "Verwendungszweck: Empfänger: John Doe"
        result = parse_key_value_string(input_str)

        assert result["Verwendungszweck"] == ""
        assert result["Empfänger"] == "John Doe"

    def test_all_keys_present(self):
        """Test parsing when all keys are present."""
        input_parts = [f"{key}: value{i}" for i, key in enumerate(KEYS)]
        input_str = " ".join(input_parts)
        result = parse_key_value_string(input_str)

        for i, key in enumerate(KEYS):
            assert result[key] == f"value{i}"

    def test_unknown_key_ignored(self):
        """Test that unknown keys are ignored."""
        input_str = "UnknownKey: some value Verwendungszweck: Test payment"
        result = parse_key_value_string(input_str)

        assert result["Verwendungszweck"] == "Test payment"
        assert "UnknownKey" not in result

    def test_value_contains_colon(self):
        """Test parsing when a value contains a colon."""
        input_str = "Verwendungszweck: Time is 12:30 Empfänger: John Doe"
        result = parse_key_value_string(input_str)

        assert result["Verwendungszweck"] == "Time is 12:30"
        assert result["Empfänger"] == "John Doe"

    def test_duplicate_keys(self):
        """Test parsing when a key appears multiple times (last one wins)."""
        input_str = "Verwendungszweck: First value Verwendungszweck: Second value"
        result = parse_key_value_string(input_str)

        assert result["Verwendungszweck"] == "Second value"

    def test_special_characters_in_value(self):
        """Test parsing values with special characters."""
        input_str = (
            "Verwendungszweck: Payment #123 @2024 (urgent!) Empfänger: Müller & Co."
        )
        result = parse_key_value_string(input_str)

        assert result["Verwendungszweck"] == "Payment #123 @2024 (urgent!)"
        assert result["Empfänger"] == "Müller & Co."

    def test_return_type(self):
        """Test that the function returns a dictionary with all expected keys."""
        result = parse_key_value_string("Verwendungszweck: Test")

        assert isinstance(result, dict)
        assert len(result) == len(KEYS)
        assert all(key in result for key in KEYS)

    def test_text_before_first_key(self):
        """Test that text before the first key is ignored."""
        input_str = "Some random text here Verwendungszweck: Test payment"
        result = parse_key_value_string(input_str)

        assert result["Verwendungszweck"] == "Test payment"

    def test_similar_key_names(self):
        """Test parsing when keys have similar prefixes."""
        # Testing keys like "Empfänger" and "IBAN Empfänger"
        input_str = (
            "IBAN Empfänger: DE123456 BIC Empfänger: DEUTDEFF Empfänger: John Doe"
        )
        result = parse_key_value_string(input_str)

        assert result["IBAN Empfänger"] == "DE123456"
        assert result["BIC Empfänger"] == "DEUTDEFF"
        assert result["Empfänger"] == "John Doe"

    def test_numeric_values(self):
        """Test parsing numeric values."""
        input_str = "Originalbetrag: 1234.56"
        result = parse_key_value_string(input_str)

        assert result["Originalbetrag"] == "1234.56"
