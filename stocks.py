import statistics

import arrow


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
