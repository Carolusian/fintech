import os
import pandas as pd
import threading
import yfinance as yf
from datetime import datetime


def get_hk_stock_symbols(file_path):
    df = pd.read_csv(file_path, skiprows=2, dtype = {'Stock Code': str})
    df = df[df['Category'] == 'Equity']
    df['sym'] = df['Stock Code'].str.extract('(?P<digital>[\d]{4}$)', expand=False)
    df['sym'] = df['sym'].astype(str) + '.HK'
    return df['sym'].tolist()


def create_dirs(dir):
    home_dir = os.path.expanduser('~')
    main_dir = os.path.join(home_dir, 'stock_data', dir)
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
    return main_dir


class StockData(threading.Thread):
    def __init__(self, sym, start_date):
        self.sym = sym
        self.start_date = start_date
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.folder_name = 'hk'
        threading.Thread.__init__(self)

    def run(self):
        print('# start getting data for %s' % self.sym)
        self.get_prices()

    def get_prices(self):
        cache_dir = create_dirs(self.folder_name)

        stock_handler = yf.Ticker(self.sym)
        try:
            data = stock_handler.history(period='max')
            df = pd.DataFrame.from_dict(data)
            df.to_csv(os.path.join(cache_dir, self.sym + '.csv'))
            return self.sym, data
        except Exception:
            print('# Error in downloading {}'.format(self.sym))
            return None

symbols = get_hk_stock_symbols(os.path.join(os.getcwd(), '2019-12-03_FullListOfSecuritiesHK.csv'))

# Break symbols in buckets in size of 10 each
# Then download stockdata with multi-threading
for i in range(0, len(symbols), 10):
    threads = []
    end = i + 10 if i + 10 < len(symbols) else len(symbols)
    for j in range(i, end):
        thread = StockData(symbols[j], '2017-01-01')
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
