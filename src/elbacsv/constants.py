"""
Constants used throughout the elbacsv package.

This module defines the recognized keys in ELBA CSV files along with their
column order indices.
"""

KEYS = {
    "Kartenzahlung mit Kartenfolge-Nr.": 4,
    "Urspr. Zahlungspflichtigenkennung": 17,
    "IBAN Transaktionsteilnehmer": 19,
    "BIC Transaktionsteilnehmer": 20,
    "IBAN Zahlungsempfänger": 9,
    "BIC Zahlungsempfänger": 10,
    "Urspr. Zahlungspflichtige": 16,
    "Auftraggeberreferenz": 12,
    "Zahlungspflichtigenkennung": 18,
    "Empfänger-Kennung": 6,
    "IBAN Auftraggeber": 13,
    "BIC Auftraggeber": 14,
    "IBAN Empfänger": 7,
    "BIC Empfänger": 8,
    "Verwendungszweck": 1,
    "Zahlungsreferenz": 2,
    "Originalbetrag": 21,
    "Auftraggeber": 11,
    "Urspr. Empfänger": 15,
    "Entgeltzeile": 22,
    "Empfänger": 5,
    "Mandat": 3,
}
