import csv
from collections import defaultdict
from decimal import Decimal

import arrow

from constants import FORMATS_DATE_ARROW

csv_file_name = 'stocks.csv'

def read_csv():
    data = defaultdict(dict)
    with open(csv_file_name) as f:
        reader = csv.DictReader(f)

        for row in reader:
            stock_date = arrow.get(row['StockDate'], FORMATS_DATE_ARROW)

            data[row['StockName'].upper()].update({
                stock_date: Decimal(row['StockPrice'])
            })
    return data

def __main__():
    stock_data = read_csv()
