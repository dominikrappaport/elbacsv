# ELBA CSV Tool

## Author

Dominik Rappaport, dominik@rappaport.at

## Motivation

I used a tool called [iFinance](http://www.ifinance.de/) to manage my bank account. iFinance has a feature to download the data automatically
via an API provider. In the past they could use two API providers, [Tink](https://tink.com/) and [Plaid](https://plaid.com/). My bank, Raiffeisen
bank in Austria, was available via Tink only. Unfortunately, staring with iFinance version 5.4, the dropped support for Tink and focused on Plaid
only. That left me with a the problem that iFinance could not download the data from my bank account any more. According to their support Plaid
will support more banks in the future but the statement was very vague and the timeline most unclear. Apparently they anticipated customer dissatisfaction
and annoucned proactively that they would return the money to all buyers who couldn't work with Plaid only support. As I already had organised
my transactions for a while using iFinance, I didn't want to go that route but decided to use the CSV import function instead.

Of course, ELBA, my bank's web banking system, does support CSV export. However, the file they create isn't ideally formatted to say the least.

### Issue #1: Missing column headers

Typically, the first line of a CSV file contains the column headers. ELBA's CSV export doesn't contain any column headers. You therefore need to
guess what the columns are. But that is not too difficult and adding a proper header is easy.

### Issue #2: Data not in first normal form

Most of the transation's data is put into a single column. This column is a string of key-value pairs. Unfortunately, the key-value pairs are
not separated by a comma and the key may contain a whitespace. An example says more than a thousand words:

```aiignore
Verwendungszweck: BILLA DANKT 0003750 STOCKERAU 2000 Zahlungsreferenz: POS          50,26 AT  D5   23.08. 18:00 Kartenzahlung mit Kartenfolge-Nr.: 5
```

In the language of relational databases, they would say the data is not in the "first normal form."
If you try to parse this field automatically you face a challenge. The code cannot tell if the rightmost key is "Kartenfolge-Nr." or if the two words
"Kartenfolge" and "Nr." are part of the key. The only way is to look for all possible keys and programme them into a list that is subsequently used
to parse the data. What keys are possible is nowhere documented. At least I was not able to find any related information.

To get properly formatted data that can be easily imported into iFinance (or Excel) I decided to write a small tool that does the job for me.

## Installation

To use my little tool for yourself you need to clone the repository and install the dependencies.

```bash
git clone https://github.com/dominikrappaport/elbacsv.git
cd elba-csv-tool
uv sync
```

These steps assume you are using [uv](https://github.com/astral-sh/uv) as your package and project manager.

## Usage

