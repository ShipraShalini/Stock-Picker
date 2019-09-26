import csv
import difflib
import os
import sys
from collections import defaultdict
from decimal import Decimal

import arrow
from arrow.parser import ParserError

from constants import FORMATS_DATE_ARROW


class UserInput:

    BOOL_DICT = {'y': True}
    NO_OF_MATCHES = 5

    OPTION_NONE = 'None of these.'

    MESSAGE_STOCK_NAME = 'Which stock you need to process:\t'
    MESSAGE_START_DATE = 'From which date you want to start:\t'
    MESSAGE_END_DATE = 'Till which date you want to analyze:\t'
    MESSAGE_SUGGESTION = 'Sorry! Did you mean any of the following?'
    MESSAGE_NOT_FOUND = (
        'Sorry! Data for stock "{}" is not present.\n'
        'Would you like to process any other stock? '
        '(Y or N):\t'
    )
    MESSAGE_TRY_AGAIN = 'Would you like to try again? (Y or N):\t'

    MESSAGE_ENTER_STOCK_NUMBER = 'Please enter the stock number:\t'
    MESSAGE_ENTER_VALID_OPTION = 'Please enter a valid option:\t'
    MESSAGE_ENTER_VALID_DATE = 'Please enter a valid date:\t'

    def __init__(self, stock_names):
        self.stock_names = stock_names

    def __call__(self):
        name = self.get_stock_name()
        start_date, end_date = self.get_dates()
        return {
            'name': name,
            'start_date': start_date,
            'end_date': end_date
        }

    def get_stock_name(self):
        name = input(self.MESSAGE_STOCK_NAME).upper()
        if name in self.stock_names:
            return name
        close_matches = difflib.get_close_matches(name, self.stock_names,
                                                  self.NO_OF_MATCHES)
        if not close_matches:
            self._repeat_or_abort(self.MESSAGE_NOT_FOUND.format(name))

        print(self.MESSAGE_SUGGESTION)
        print('0: {}'.format(self.OPTION_NONE))
        for i, match in enumerate(close_matches, start=1):
            print('{}: {}'.format(i, match))

        message = self.MESSAGE_ENTER_STOCK_NUMBER
        while True:
            try:
                stock_number = int(input(message))
                if stock_number == 0:
                    self._repeat_or_abort(self.MESSAGE_TRY_AGAIN)
                return close_matches[stock_number - 1]
            except (ValueError, IndexError):
                message = self.MESSAGE_ENTER_VALID_OPTION

    def get_dates(self):
        start_date = self._get_date(self.MESSAGE_START_DATE)
        end_date = self._get_date(self.MESSAGE_END_DATE)

        if start_date > end_date:
            return end_date, start_date
        return start_date, end_date

    def _get_date(self, message):
        while True:
            date_str = input(message)
            try:
                return arrow.get(date_str, FORMATS_DATE_ARROW)
            except (ParserError, ValueError):
                message = self.MESSAGE_ENTER_VALID_DATE

    def _repeat_or_abort(self, message):
        if not self._get_boolean_answer(message):
            self._abort()
        self.get_stock_name()

    @staticmethod
    def _abort():
        sys.exit(1)

    def _get_boolean_answer(self, message):
        choice = input(message).lower()
        return self.BOOL_DICT.get(choice, False)


class CSVInput:
    MESSAGE_INPUT_FILE_PATH = (
        'Please input a valid file path or press ENTER to abort: \t'
    )
    MESSAGE_NOT_FOUND = 'The file "{}" does not exists. '
    MESSAGE_NO_DATA = 'The file "{}" is empty or not a valid csv file. '

    def read(self, csv_file_path):
        csv_file_path = self.get_csv_file(csv_file_path)

        data = defaultdict(dict)
        with open(csv_file_path) as f:
            reader = csv.DictReader(f)

            for row in reader:
                stock_date = arrow.get(row['StockDate'], FORMATS_DATE_ARROW)

                data[row['StockName'].upper()].update({
                    stock_date: Decimal(row['StockPrice'])
                })
        if not data:
            print(self.MESSAGE_NO_DATA.format(csv_file_path))
            self.read(csv_file_path=None)
        return data

    def get_csv_file(self, csv_file):
        if not csv_file:
            csv_file = input(self.MESSAGE_INPUT_FILE_PATH)

        while True:
            if not csv_file:
                self._abort()
            if os.path.isfile(csv_file):
                return csv_file
            csv_file = input(
                self.MESSAGE_NOT_FOUND.format(csv_file) + self.MESSAGE_INPUT_FILE_PATH
            )

    @staticmethod
    def _abort():
        sys.exit(1)
