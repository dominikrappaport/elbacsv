import csv

import pytest

from elbacsv import (
    KEYS,
    main,
    parse_command_line_args,
    parse_key_value_string,
    process_csv_file,
    strip_zwnbsp,
)


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


class TestStripZwnbsp:
    """Test suite for the strip_zwnbsp function."""

    def test_string_with_zwnbsp(self):
        """Test removing ZWNBSP from a string."""
        input_str = "\ufeffHello\ufeffWorld\ufeff"
        result = strip_zwnbsp(input_str)
        assert result == "HelloWorld"

    def test_string_without_zwnbsp(self):
        """Test that strings without ZWNBSP are unchanged."""
        input_str = "Hello World"
        result = strip_zwnbsp(input_str)
        assert result == "Hello World"

    def test_empty_string(self):
        """Test with an empty string."""
        result = strip_zwnbsp("")
        assert result == ""

    def test_non_string_input(self):
        """Test that non-string inputs are returned unchanged."""
        assert strip_zwnbsp(123) == 123
        assert strip_zwnbsp(None) is None
        assert strip_zwnbsp([1, 2, 3]) == [1, 2, 3]
        assert strip_zwnbsp({"key": "value"}) == {"key": "value"}

    def test_string_with_multiple_zwnbsp(self):
        """Test removing multiple ZWNBSP characters."""
        input_str = "\ufeff\ufeff\ufeffTest\ufeff\ufeff"
        result = strip_zwnbsp(input_str)
        assert result == "Test"


class TestProcessCsvFile:
    """Test suite for the process_csv_file function."""

    def test_process_simple_csv(self, tmp_path):
        """Test processing a simple CSV file."""
        # Create a temporary input CSV file
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        # Write test data
        input_file.write_text(
            "2024-01-15,Verwendungszweck: Test payment Empfänger: John Doe,2024-01-15,100.00,EUR,2024-01-15 10:00:00\n",
            encoding="utf-8",
        )

        # Process the file
        process_csv_file(str(input_file), str(output_file), False)

        # Read and verify output
        output_content = output_file.read_text(encoding="utf-8")
        assert "Durchführungsdatum" in output_content
        assert "Test payment" in output_content
        assert "John Doe" in output_content

    def test_process_csv_with_merge(self, tmp_path):
        """Test processing a CSV file with merge option."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        # Write test data with both Zahlungsreferenz and Verwendungszweck
        input_file.write_text(
            "2024-01-15,Zahlungsreferenz: REF123 Verwendungszweck: Payment,2024-01-15,100.00,EUR,2024-01-15 10:00:00\n",
            encoding="utf-8",
        )

        # Process with merge=True
        process_csv_file(str(input_file), str(output_file), merge=True)

        # Read and verify output
        output_content = output_file.read_text(encoding="utf-8")
        assert "Zahlungsreferenz" not in output_content  # Should be removed
        assert "REF123 Payment" in output_content  # Should be merged

    def test_process_csv_preserves_other_columns(self, tmp_path):
        """Test that processing preserves other columns."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        input_file.write_text(
            "2024-01-15,Verwendungszweck: Test,2024-01-16,200.50,USD,2024-01-15 12:00:00\n",
            encoding="utf-8",
        )

        process_csv_file(str(input_file), str(output_file), False)

        output_content = output_file.read_text(encoding="utf-8")
        assert "2024-01-15" in output_content
        assert "2024-01-16" in output_content
        assert "200.50" in output_content
        assert "USD" in output_content

    def test_process_csv_with_zwnbsp(self, tmp_path):
        """Test that ZWNBSP characters are removed from output."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        # Write test data with ZWNBSP
        input_file.write_text(
            "\ufeff2024-01-15,Verwendungszweck: \ufeffTest\ufeff,2024-01-15,100.00,EUR,2024-01-15 10:00:00\n",
            encoding="utf-8",
        )

        process_csv_file(str(input_file), str(output_file), False)

        output_content = output_file.read_text(encoding="utf-8")
        assert "\ufeff" not in output_content

    def test_process_csv_multiple_rows(self, tmp_path):
        """Test processing multiple rows."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        input_data = (
            "2024-01-15,Verwendungszweck: Payment 1,2024-01-15,100.00,EUR,2024-01-15 10:00:00\n"
            "2024-01-16,Verwendungszweck: Payment 2,2024-01-16,200.00,EUR,2024-01-16 11:00:00\n"
        )
        input_file.write_text(input_data, encoding="utf-8")

        process_csv_file(str(input_file), str(output_file), False)

        output_lines = output_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(output_lines) == 3  # Header + 2 data rows

    def test_process_csv_empty_values(self, tmp_path):
        """Test processing with empty key values."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        input_file.write_text(
            "2024-01-15,,2024-01-15,100.00,EUR,2024-01-15 10:00:00\n",
            encoding="utf-8",
        )

        process_csv_file(str(input_file), str(output_file), False)

        # Should complete without error
        assert output_file.exists()

    def test_process_csv_column_order(self, tmp_path):
        """Test that columns are written in the correct order."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        # Write test data with multiple keys
        input_file.write_text(
            "2024-01-15,Verwendungszweck: Test Zahlungsreferenz: REF123 Empfänger: John Doe,2024-01-16,100.00,EUR,2024-01-15 10:00:00\n",
            encoding="utf-8",
        )

        process_csv_file(str(input_file), str(output_file), False)

        # Read the header row
        with open(output_file, encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)

        # Expected column order
        sorted_keys = sorted(KEYS.keys(), key=lambda k: KEYS[k])
        expected_header = [
            "Durchführungsdatum",
            *sorted_keys,
            "Valutadatum",
            "Betrag",
            "Währung",
            "Zeitstempel",
        ]

        assert header == expected_header

        # Verify specific positions
        assert header[0] == "Durchführungsdatum"
        assert header[1] == "Verwendungszweck"  # KEYS value: 1
        assert header[2] == "Zahlungsreferenz"  # KEYS value: 2
        assert header[3] == "Mandat"  # KEYS value: 3
        assert header[-4] == "Valutadatum"
        assert header[-3] == "Betrag"
        assert header[-2] == "Währung"
        assert header[-1] == "Zeitstempel"


class TestParseCommandLineArgs:
    """Test suite for the parse_command_line_args function."""

    def test_basic_arguments(self, monkeypatch):
        """Test parsing basic input and output arguments."""
        monkeypatch.setattr("sys.argv", ["elbacsv.py", "input.csv", "output.csv"])

        args = parse_command_line_args()
        assert args.input_csv == "input.csv"
        assert args.output_csv == "output.csv"
        assert args.merge is False

    def test_merge_argument(self, monkeypatch):
        """Test parsing with --merge flag."""
        monkeypatch.setattr(
            "sys.argv", ["elbacsv.py", "input.csv", "output.csv", "--merge"]
        )

        args = parse_command_line_args()
        assert args.input_csv == "input.csv"
        assert args.output_csv == "output.csv"
        assert args.merge is True

    def test_missing_arguments(self, monkeypatch):
        """Test that missing required arguments raises SystemExit."""
        monkeypatch.setattr("sys.argv", ["elbacsv.py"])

        with pytest.raises(SystemExit):
            parse_command_line_args()


class TestMain:
    """Test suite for the main function."""

    def test_main_execution(self, tmp_path, monkeypatch):
        """Test that main executes without errors."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        input_file.write_text(
            "2024-01-15,Verwendungszweck: Test,2024-01-15,100.00,EUR,2024-01-15 10:00:00\n",
            encoding="utf-8",
        )

        monkeypatch.setattr(
            "sys.argv", ["elbacsv.py", str(input_file), str(output_file)]
        )

        main()

        assert output_file.exists()

    def test_main_with_merge(self, tmp_path, monkeypatch):
        """Test main with merge flag."""
        input_file = tmp_path / "input.csv"
        output_file = tmp_path / "output.csv"

        input_file.write_text(
            "2024-01-15,Zahlungsreferenz: REF Verwendungszweck: Test,2024-01-15,100.00,EUR,2024-01-15 10:00:00\n",
            encoding="utf-8",
        )

        monkeypatch.setattr(
            "sys.argv", ["elbacsv.py", str(input_file), str(output_file), "--merge"]
        )

        main()

        assert output_file.exists()
        output_content = output_file.read_text(encoding="utf-8")
        assert "REF Test" in output_content
