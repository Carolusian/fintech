import os
import pandas as pd
import threading
from datetime import datetime
from yahoo_finance import Share


def get_hk_stock_symbols(file_path):
    df = pd.read_csv(file_path, header=None,
                     names=['id', 'sym', 'name_zh', 'name_cn'],
                     dtype={
                         'sym': str
                     })
    df = df[df['sym'].str.startswith('0')]
    df['sym'] = df['sym'].str.extract('(?P<digital>[\d]{4}$)', expand=False)
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

        stock_handler = Share(self.sym)
        try:
            data = stock_handler.get_historical(self.start_date, self.end_date)
            df = pd.DataFrame.from_dict(data)
            df.to_csv(os.path.join(cache_dir, self.sym))
            return self.sym, data
        except Exception:
            print('# Error in downloading {}'.format(self.sym))
            return None

symbols = get_hk_stock_symbols(os.path.join(os.getcwd(), 'hk_securities.csv'))

# Break symbols in buckets in size of 10 each
# Then download stockdata with multi-threading
for i in range(0, len(symbols), 10):
    threads = []
    for j in range(i, i+10):
        thread = StockData(symbols[j], '2012-01-01')
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
