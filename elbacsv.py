import csv
import argparse
import re


KEYS = [
    "Zahlungsreferenz",
    "Verwendungszweck",
    "Kartenzahlung mit Kartenfolge-Nr.",
    "IBAN Empfänger",
    "BIC Empfänger",
    "IBAN Auftraggeber",
    "BIC Auftraggeber",
    "IBAN Zahlungsempfänger",
    "BIC Zahlungsempfänger",
    "Empfänger-Kennung",
    "Auftraggeberreferenz",
    "Mandat",
    "Empfänger",
    "MandatsID",
    "CreditorID",
    "Entgeltzeile",
    "Originalbetrag",
    "Urspr. Zahlungspflichtige",
    "Urspr. Zahlungspflichtigenkennung",
    "Zahlungspflichtigenkennung", # TODO: Change code so it makes key detection greedy
]

def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description="Process an ELBA-generated CSV file and write results to an output CSV file."
    )

    parser.add_argument(
        "input_csv",
        help="Path to the input CSV file."
    )

    parser.add_argument(
        "output_csv",
        help="Path to the output CSV file."
    )

    return parser.parse_args()


def parse_key_value_string(s: str):
    """Parse a string into a dict of key: value pairs based on the given list of keys."""
    result = {k: "" for k in KEYS}

    # Sort keys by length descending (avoid partial matches)
    keys_sorted = sorted(KEYS, key=len, reverse=True)
    # Build regex: (Key1|Key2|Key3):
    pattern = r"(" + "|".join(map(re.escape, keys_sorted)) + r")\s*:\s*"
    parts = re.split(pattern, s)

    it = iter(parts[1:])  # skip text before first key
    for key, value in zip(it, it):
        result[key.strip()] = value.strip()

    return result


def process_csv_file(input_csv, output_csv):
    with open(input_csv, newline="", encoding="utf-8") as f:
        sample = f.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        f.seek(0)
        reader = csv.reader(f, dialect)
        rows = list(reader)

    second_col_index = 1
    new_header = ["Datum1"] + KEYS + ["Datum2", "Betrag", "Währung", "Zeitstempel"]

    new_rows = []
    for row in rows:
        kv_dict = parse_key_value_string(row[second_col_index])
        new_row = row[:second_col_index] + [kv_dict[k] for k in KEYS] + row[second_col_index + 1:]
        new_rows.append(new_row)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, dialect)
        writer.writerow(new_header)
        writer.writerows(new_rows)


def main():
    args = parse_command_line_args()

    process_csv_file(args.input_csv, args.output_csv)


if __name__ == "__main__":
    main()
