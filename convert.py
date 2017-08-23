from datetime import datetime
import csv


with open('transactions.csv', 'r') as f, open('output.csv', 'w') as out:
    fieldnames = (
        'iban',
        'currency',
        'interest_date',
        'by_af_code',
        'amount',
        'against_bill',
        'to_name',
        'book_date',
        'book_code',
        'filler',
        'desc_1',
        'desc_2',
        'desc_3',
        'desc_4',
        'desc_5',
        'desc_6',
        'end_to_end_id',
        'id_to_account',
        'mandate_id',

    )
    reader = csv.DictReader(f, fieldnames=fieldnames)
    writer = csv.writer(out)

    writer.writerow(('Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow'))
    for row in reader:
        date = datetime.strptime(row['interest_date'], '%Y%m%d')
        date = date.strftime('%d/%m/%Y')
        if row['to_name']:
            payee = row['to_name']
            memo = ''.join((row['desc_1'], row['desc_2'], row['desc_3'], row['desc_4'], row['desc_5']))
        else:
            payee = row['desc_1']
            memo = ''.join((row['desc_2'], row['desc_3'], row['desc_4'], row['desc_5']))

        if row['by_af_code'] == 'D':
            outflow = row['amount']
            inflow = ''
        else:
            inflow = row['amount']
            outflow = ''

        writer.writerow((date, payee, '', memo, outflow, inflow))
