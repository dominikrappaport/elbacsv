"""
ELBA CSV Tool - Parse and process ELBA CSV exports.

This package provides functionality to parse CSV files exported from ELBA
(Austrian banking software), extract key-value pairs from structured text,
and write the parsed data to a new CSV file with expanded columns.

Author: Dominik Rappaport, dominik@rappaport.at
"""

from .cli import main, parse_command_line_args
from .constants import KEYS
from .core import parse_key_value_string, process_csv_file, strip_zwnbsp

__version__ = "0.1.1"
__author__ = "Dominik Rappaport"
__email__ = "dominik@rappaport.at"
__license__ = "MIT"
__url__ = "https://github.com/dominikrappaport/elbacsv"
__description__ = "A small utility that cleans and normalizes CSV exports from Raiffeisen Bank’s ELBA online banking system, making them compatible with iFinance and other financial tools"
__keywords__ = "download strava leaderboards screen-scraping"
__package_name__ = "elbacsv"
__readme_name__ = "README.md"

__all__ = [
    "KEYS",
    "main",
    "parse_command_line_args",
    "parse_key_value_string",
    "process_csv_file",
    "strip_zwnbsp",
]
