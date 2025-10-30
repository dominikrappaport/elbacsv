"""
Command-line interface for the elbacsv package.

This module handles command-line argument parsing and provides
the main entry point for the CLI tool.
"""

import argparse

from .core import process_csv_file


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

    parser.add_argument(
        "--merge",
        help="Merge 'Zahlungsreferenz', 'Verwendungszweck' and 'Auftraggeberreferenz'",
        action="store_true",
    )

    return parser.parse_args()


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
