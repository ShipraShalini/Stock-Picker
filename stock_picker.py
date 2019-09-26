import csv
from collections import defaultdict
from decimal import Decimal

import arrow

from constants import FORMATS_DATE_ARROW
from stocks import Stock
from userinput import UserInput

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


if __name__ == "__main__":
    all_stock_data = read_csv()
    user_input = UserInput(list(all_stock_data.keys()))()
    stock_records = all_stock_data[user_input['name']]
    stock = Stock(stock_records,
                  user_input['start_date'],
                  user_input['end_date'])
    stock.print_all_data()
