import csv
import difflib
import statistics
from collections import defaultdict
from decimal import Decimal

import arrow

csv_file_name = 'stocks.csv'

FORMATS_DATE_ARROW = [
    'D-M-YY', 'D/M/YY', 'D.M.YY',
    'D-MMM-YY', 'D/MMM/YY', 'D.MMM.YY',
    'YY-M-D', 'YY/M/D', 'YY.M.D',
    'YY-MMM-D', 'YY/MMM/D', 'YY.MMM.D'
]

def get_date(stock_date):
    return arrow.get(stock_date, FORMATS_DATE_ARROW)


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

def get_stock_name(name):
    pass


class UserInput:

    BOOL_DICT = {'y': True}
    NO_OF_MATCHES = 5

    OPTION_NONE = 'None of these.'

    MESSAGE_STOCK_NAME = 'Which stock you need to process:\t'
    MESSAGE_START_DATE = 'From which date you want to start:\t'
    MESSAGE_END_DATE = 'Till which date you want to analyze:\t'
    MESSAGE_SUGGESTION = 'Sorry! Did you mean any of the following?'
    MESSAGE_NOT_FOUND = ('Sorry! Data for {} is not present. Would you like '
                         'to process any other stock? (Y or N):\t')
    MESSAGE_TRY_AGAIN = 'Would you like to try again? (Y or N):\t'

    MESSAGE_ENTER_STOCK_NUMBER =  'Please enter the stock number:\t'
    MESSAGE_ENTER_VALID_OPTION = 'Please enter a valid option.'


    def __init__(self, stock_names):
        self.stock_names = stock_names

    def abort(self):
        pass

    def get_stock_name(self):
        name = input(self.MESSAGE_STOCK_NAME).upper()
        if name in self.stock_names:
            return name
        close_matches = difflib.get_close_matches(name, self.stock_names,
                                                  self.NO_OF_MATCHES)
        if not close_matches:
            if self._get_boolean_answer(self.MESSAGE_NOT_FOUND):
                self.get_stock_name()
            self.abort()

        print(self.MESSAGE_SUGGESTION)
        print('0: {}'.format(self.OPTION_NONE))
        for i, match in enumerate(close_matches, start=1):
            print('{}: {}'.format(i, match))

        message = self.MESSAGE_ENTER_STOCK_NUMBER
        while True:
            try:
                stock_number = int(input(message))
                break
            except ValueError:
                message = self.MESSAGE_ENTER_VALID_OPTION

        if stock_number == 0:
            if self._get_boolean_answer(self.MESSAGE_TRY_AGAIN):
                self.get_stock_name()
            self.abort()
        return close_matches[stock_number - 1]

    def get_start_date(self):


    def _get_date(self, message):
        date_str = input(message)
        return arrow.get(date_str, FORMATS_DATE_ARROW)

    def _get_boolean_answer(self, message):
        choice = input(message).lower()
        return self.BOOL_DICT.get(choice, False)


class Stock:
    DEFAULT_STOCK_UNITS = 100

    def __init__(self, name, start_date, end_date):
        self.records = self._get_records(name, start_date, end_date)

    def get_stats(self, records):
        data = records.values()
        return {
            'std': statistics.stdev(data),
            'mean': statistics.mean(data)
        }

    def get_transaction_data(self, records):
        date_sell = max(records.keys(), key=(lambda k: records[k]))
        date_buy = min(records.keys(), key=(lambda k: records[k]))

        price_sell = records[date_sell]
        price_buy = records[date_buy]

        profit = (price_sell - price_buy) * 100
        return {
            'sell_date': date_sell.format('DD-MMM-YYYY'),
            'buy_date': date_buy.format('DD-MMM-YYYY'),
            'profit': 'Rs. {}'.format(str(profit)),
        }

    def print_all_data(self, records):
        data = {
            **self.get_stats(records),
            **self.get_transaction_data(records)
        }

        for key, value in data.items():
            print('{}: {}'.format(key, value))

    def _get_initial_price(self, stock_records, start_date):
        while True:
            rec = stock_records[start_date]
            if rec:
                return rec
            start_date = start_date.shift(days=-1)

    def _get_records(self, stock_records, start_date, end_date):
        records = {}

        curr_date = arrow.get(start_date)
        end_date = arrow.get(end_date)

        current_price = self._get_initial_price(stock_records, start_date)

        while curr_date < end_date:
            price = records.get(curr_date)
            if not price:
                price = current_price
            else:
                current_price = price

            records[curr_date] = price
            curr_date = curr_date.shift(days=1)
        return records

    @staticmethod
    def _snake_to_title(string):
        return string.replace('_', ' ').title()


def __main__():
    stock_data = read_csv()
