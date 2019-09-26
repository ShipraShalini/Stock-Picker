import argparse

from stocks import Stock
from userinput import CSVInput, UserInput


parser = argparse.ArgumentParser(conflict_handler='resolve')
parser.add_argument('csv_file', nargs='?', default=None,
                    help="CSV file path")
args = parser.parse_args()

csv_file = args.csv_file


if __name__ == "__main__":
    all_stock_data = CSVInput().read(csv_file)
    user_input = UserInput(list(all_stock_data.keys()))()
    stock_records = all_stock_data[user_input['name']]
    stock = Stock(stock_records,
                  user_input['start_date'],
                  user_input['end_date'])
    stock.print_all_data()
