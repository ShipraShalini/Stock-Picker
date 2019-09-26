import statistics

import arrow


class Stock:
    DEFAULT_STOCK_UNITS = 100
    MESSAGE_RESULT = '\nHere is the info that you requested:\n'

    def __init__(self, stock_records, start_date, end_date):
        self.interval_records = self._get_records(stock_records,
                                                  start_date, end_date)

    def get_stats(self):
        data = self.interval_records.values()
        return {
            'std': round(statistics.stdev(data), 3),
            'mean': round(statistics.mean(data), 3)
        }

    def get_transaction_data(self):

        date_sell = max(self.interval_records.keys(), key=(lambda k: self.interval_records[k]))
        date_buy = min(self.interval_records.keys(), key=(lambda k: self.interval_records[k]))

        price_sell = self.interval_records[date_sell]
        price_buy = self.interval_records[date_buy]

        profit = (price_sell - price_buy) * self.DEFAULT_STOCK_UNITS
        return {
            'sell_date': date_sell.format('DD-MMM-YYYY'),
            'buy_date': date_buy.format('DD-MMM-YYYY'),
            'profit': 'Rs. {}'.format(str(profit)),
        }

    def print_all_data(self):
        data = {
            **self.get_stats(),
            **self.get_transaction_data()
        }
        print(self.MESSAGE_RESULT)
        for key, value in data.items():
            print('{}: {}'.format(self._snake_to_title(key), value))

    def _get_start_date_price(self, stock_records, start_date):
        curr_date = start_date
        min_date = min(stock_records.keys())
        while min_date <= curr_date:
            price = stock_records.get(curr_date)
            if price:
                return price
            curr_date = curr_date.shift(days=-1)

        curr_date = start_date
        max_date = max(stock_records.keys())
        while max_date > curr_date:
            price = stock_records.get(curr_date)
            if price:
                return price
            curr_date = curr_date.shift(days=1)

    def _get_records(self, stock_records, start_date, end_date):
        records = {}

        curr_date = arrow.get(start_date)
        end_date = arrow.get(end_date)

        current_price = self._get_start_date_price(stock_records, start_date)

        while curr_date < end_date:
            price = stock_records.get(curr_date)
            if price:
                current_price = price
            else:
                price = current_price

            records[curr_date] = price
            curr_date = curr_date.shift(days=1)
        return records

    @staticmethod
    def _snake_to_title(string):
        return string.replace('_', ' ').title()
