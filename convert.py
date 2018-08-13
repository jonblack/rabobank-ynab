import argparse
import csv
import sys

from datetime import datetime

def convert(rabobank_csvfile, output_csvfile):
    with rabobank_csvfile as f, output_csvfile as out:
        fieldnames = (
            'IBAN/BBAN',
            'Munt',
            'BIC',
            'Volgnr',
            'Datum',
            'Rentedatum',
            'Bedrag',
            'Saldo na trn',
            'Tegenrekening IBAN/BBAN',
            'Naam tegenpartij',
            'Naam uiteindelijke partij',
            'Naam initi�rende partij',
            'BIC tegenpartij',
            'Code',
            'Batch ID',
            'Transactiereferentie',
            'Machtigingskenmerk',
            'Incassant ID',
            'Betalingskenmerk',
            'Omschrijving-1',
            'Omschrijving-2',
            'Omschrijving-3',
            'Reden retour',
            'Oorspr bedrag',
            'Oorspr munt',
            'Koers'
        )

        reader = csv.DictReader(f, fieldnames=fieldnames)
        next(reader, None) # skip header
        writer = csv.writer(out)
        writer.writerow(('Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow'))
        for row in reader:
            date = convert_date(row['Datum'])
            payee = row['Naam tegenpartij']
            memo = ''.join((row['Omschrijving-1'], row['Omschrijving-2'], row['Omschrijving-3']))

            if row['Bedrag'][0] == '+':
                outflow = 0
                inflow = row['Bedrag'][1:].replace(',', '.')
            else:
                outflow = row['Bedrag'][1:].replace(',', '.')
                inflow = 0

            writer.writerow((date, payee, '', memo, outflow, inflow))


def convert_date(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%d/%m/%Y')


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'rabobank_csvfile',
        type=argparse.FileType('r', encoding='ISO-8859-1')
    )
    parser.add_argument(
        'output_csvfile',
        nargs='?',
        type=argparse.FileType('w', encoding='ISO-8859-1'),
        default=sys.stdout
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_cli_args()
    convert(args.rabobank_csvfile, args.output_csvfile)
