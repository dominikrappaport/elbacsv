# ELBA CSV Tool

## Author

Dominik Rappaport, dominik@rappaport.at

## Motivation

I use a software application called [iFinance](http://www.ifinance.de/) to manage my bank accounts. iFinance includes a feature that allows automatic data downloads through an API provider. In earlier versions, the software supported two such providers: [Tink](https://tink.com/) and [Plaid](https://plaid.com/). My bank, Raiffeisen Bank in Austria, was accessible exclusively via Tink.  

Unfortunately, beginning with iFinance version 5.4, support for Tink was discontinued in favor of Plaid as the sole provider. Consequently, iFinance was no longer able to retrieve data from my bank account. According to the vendor’s support team, Plaid may expand its support to additional banks in the future, although the statement was vague and no timeline was provided. Anticipating customer dissatisfaction, the company proactively announced that it would refund users who could no longer use the product under the new limitations.  

As I had already been using iFinance for some time to organize my financial transactions, I preferred not to request a refund. Instead, I decided to continue using the software by importing data through the CSV import function.  

Naturally, ELBA — the online banking system provided by Raiffeisen Bank — supports CSV exports. However, the structure of the exported file is suboptimal for data processing purposes.  

### Issue #1: Missing column headers

In a properly formatted CSV file, the first row typically contains column headers. The CSV export from ELBA, however, omits these headers, requiring the user to manually identify and assign them. Fortunately, this is a relatively minor inconvenience and can be resolved easily.  

### Issue #2: Data not in first normal form

The majority of each transaction’s data is contained within a single column as a string of key–value pairs. Unfortunately, these pairs are not separated by commas, and the keys themselves may contain whitespace. As the following example illustrates:

```aiignore
Verwendungszweck: BILLA DANKT 0003750 STOCKERAU 2000 Zahlungsreferenz: POS          50,26 AT  D5   23.08. 18:00 Kartenzahlung mit Kartenfolge-Nr.: 5
```

In database terminology, this structure violates the first normal form (1NF).
Automated parsing of this field presents a challenge: it is not straightforward to determine whether the final key is “Kartenfolge-Nr.” or whether “Kartenfolge” and “Nr.” are separate components of the key. The only viable approach is to define a comprehensive list of all possible keys and use it as a reference for parsing the data. Unfortunately, no official documentation describing these keys appears to exist.

To obtain properly structured data suitable for import into iFinance (or tools such as Excel), I decided to develop a small utility that performs the required data transformation.

## Installation

To use my little tool for yourself you need to clone the repository and install the dependencies.

```bash
git clone https://github.com/dominikrappaport/elbacsv.git
cd elba-csv-tool
uv sync
```

These steps assume you are using [uv](https://github.com/astral-sh/uv) as your package and project manager.

## Usage

