"""
Core business logic for ELBA CSV processing.

This module contains the main parsing and processing functions
for transforming ELBA CSV files into normalized format.
"""

import csv
import re

from .constants import KEYS


def parse_key_value_string(s):
    """
    Parse a string into a dict of key: value pairs based on the given list of keys.

    Extracts structured data from a string where keys are followed by colons
    and values. The function recognizes keys defined in the global KEYS list
    and creates a dictionary with all keys, setting empty strings for missing ones.

    Args:
        s: Input string containing key-value pairs in format "Key: Value".

    Returns:
        dict[str, str]: Dictionary mapping each key from KEYS to its extracted
            value, or empty string if the key is not found in the input.

    Example:
        >>> parse_key_value_string("Empfänger: John Doe Betrag: 100")
        {'Empfänger': 'John Doe', 'Betrag': '100', ...}

    """
    result = dict.fromkeys(KEYS.keys(), "")

    # Build regex: (Key1|Key2|Key3):
    pattern = r"(" + "|".join(map(re.escape, KEYS.keys())) + r")\s*:\s*"
    parts = re.split(pattern, s)

    it = iter(parts[1:])  # skip text before first key
    for key, value in zip(it, it, strict=False):
        result[key.strip()] = value.strip()

    return result


def strip_zwnbsp(x):
    """
    Remove Zero Width No-Break Space (U+FEFF) characters from strings.

    Args:
        x: Value to process. Can be any type, but only strings are modified.

    Returns:
        If x is a string, returns the string with ZWNBSP characters removed.
        Otherwise, returns x unchanged.

    """
    return x.replace("\ufeff", "") if isinstance(x, str) else x


def process_csv_file(input_csv, output_csv, merge):
    """
    Process an ELBA CSV file and write parsed results to a new CSV file.

    Reads the input CSV file, parses the second column (index 1) which contains
    structured key-value data, expands it into separate columns based on the
    KEYS list, and writes the result to the output file.

    Args:
        input_csv: Path to the input CSV file to be processed.
        output_csv: Path to the output CSV file where results will be written.
        merge: If True, merge 'Zahlungsreferenz', 'Verwendungszweck' and 'Auftraggeberreferenz' columns.

    Note:
        The function assumes the second column (index 1) contains the structured
        data to be parsed. All other columns are preserved in their original positions.

    """
    with open(input_csv, newline="", encoding="utf-8") as f:
        sample = f.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        f.seek(0)
        reader = csv.reader(f, dialect)
        rows = list(reader)

    second_col_index = 1

    # Sort keys by their values in the KEYS dictionary
    sorted_keys = sorted(KEYS.keys(), key=lambda k: KEYS[k])

    new_header = [
        "Durchführungsdatum",
        *list(sorted_keys),
        "Valutadatum",
        "Betrag",
        "Währung",
        "Zeitstempel",
    ]

    new_rows = []
    for row in rows:
        row_data = parse_key_value_string(row[second_col_index])

        # If merge is True, combine Zahlungsreferenz, Verwendungszweck and Auftraggeberreferenz
        if merge:
            zahlungsreferenz = row_data["Zahlungsreferenz"].strip()
            verwendungszweck = row_data["Verwendungszweck"].strip()
            auftraggeberreferenz = row_data["Auftraggeberreferenz"].strip()

            # Collect all non-empty values
            merged_parts = [
                part
                for part in [zahlungsreferenz, verwendungszweck, auftraggeberreferenz]
                if part
            ]

            # Merge the fields with space separation
            row_data["Verwendungszweck"] = " ".join(merged_parts)

            # If merge is True, remove 'Zahlungsreferenz' and 'Auftraggeberreferenz' from sorted_keys
            sorted_keys = [
                k
                for k in sorted_keys
                if k not in {"Zahlungsreferenz", "Auftraggeberreferenz"}
            ]

        new_row = (
            row[:second_col_index]
            + [row_data[k] for k in sorted_keys]
            + row[second_col_index + 1 :]
        )
        new_rows.append(new_row)

    if merge:
        new_header.remove("Zahlungsreferenz")
        new_header.remove("Auftraggeberreferenz")

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, dialect)
        writer.writerow([strip_zwnbsp(v) for v in new_header])
        for row in new_rows:
            writer.writerow([strip_zwnbsp(v) for v in row])
