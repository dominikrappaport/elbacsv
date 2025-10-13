"""
Parses ELBA CSV files and processes them for easier importing.

This module reads CSV files exported from ELBA (Austrian banking software),
extracts key-value pairs from a structured text column, and writes the parsed
data to a new CSV file with expanded columns. This makes importing that data
into applications like Excel or iFinance easier.

Dominik Rappaport, dominik@rappaport.at
"""

import argparse
import csv
import re

KEYS = [
    "Kartenzahlung mit Kartenfolge-Nr.",
    "Urspr. Zahlungspflichtigenkennung",
    "IBAN Transaktionsteilnehmer",
    "Zahlungspflichtigenkennung",
    "BIC Transaktionsteilnehmer",
    "Urspr. Zahlungspflichtige",
    "IBAN Zahlungsempfänger",
    "BIC Zahlungsempfänger",
    "Auftraggeberreferenz",
    "IBAN Auftraggeber",
    "Empfänger-Kennung",
    "Zahlungsreferenz",
    "Verwendungszweck",
    "BIC Auftraggeber",
    "Urspr. Empfänger",
    "Originalbetrag",
    "IBAN Empfänger",
    "BIC Empfänger",
    "Entgeltzeile",
    "Auftraggeber",
    "Empfänger",
    "Mandat",
]


def parse_command_line_args():
    """
    Parse command-line arguments for CSV processing.

    Returns:
        Parsed arguments containing input_csv and output_csv paths.

    """
    parser = argparse.ArgumentParser(
        description="Process an ELBA-generated CSV file and write results to an output CSV file.",
    )

    parser.add_argument("input_csv", help="Path to the input CSV file.")

    parser.add_argument("output_csv", help="Path to the output CSV file.")

    parser.add_argument("--merge", help="Merge 'Zahlungsreferenz' and 'Verwendungszweck'", action="store_true")

    return parser.parse_args()


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
    result = dict.fromkeys(KEYS, "")

    # Build regex: (Key1|Key2|Key3):
    pattern = r"(" + "|".join(map(re.escape, KEYS)) + r")\s*:\s*"
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


def process_csv_file(input_csv, output_csv, merge=False):
    """
    Process an ELBA CSV file and write parsed results to a new CSV file.

    Reads the input CSV file, parses the second column (index 1) which contains
    structured key-value data, expands it into separate columns based on the
    KEYS list, and writes the result to the output file.

    Args:
        input_csv: Path to the input CSV file to be processed.
        output_csv: Path to the output CSV file where results will be written.
        merge: If True, merge 'Zahlungsreferenz' and 'Verwendungszweck' columns.

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
    new_header = ["Durchführungsdatum", *KEYS, "Valutadatum", "Betrag", "Währung", "Zeitstempel"]

    new_rows = []
    for row in rows:
        kv_dict = parse_key_value_string(row[second_col_index])
        new_row = (
            row[:second_col_index]
            + [kv_dict[k] for k in KEYS]
            + row[second_col_index + 1 :]
        )
        new_rows.append(new_row)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, dialect)
        writer.writerow([strip_zwnbsp(v) for v in new_header])
        for row in new_rows:
            writer.writerow([strip_zwnbsp(v) for v in row])


def main():
    """
    Main entry point for the CSV processing script.

    Parses command-line arguments and processes the specified input CSV file,
    writing the parsed results to the specified output CSV file.
    """
    args = parse_command_line_args()

    process_csv_file(args.input_csv, args.output_csv, args.merge)


if __name__ == "__main__":
    main()
