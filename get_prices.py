import os
import pandas as pd
import gevent
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


def get_prices(symbols, start, end, folder_name='hk'):
    cache_dir = create_dirs(folder_name)

    def get_prices_for(sym):
        stock_handler = Share(sym)
        try:
            print('# Getting data for {}...'.format(sym))
            data = stock_handler.get_historical(start, end)
            df = pd.DataFrame.from_dict(data)
            df.to_csv(os.path.join(cache_dir, sym))
            return sym, data
        except:
            print('# Error in downloading {}'.format(sym))
            return None

    jobs = [gevent.spawn(get_prices_for, sym) for sym in symbols]
    gevent.joinall(jobs)

symbols = get_hk_stock_symbols(os.path.join(os.getcwd(), 'hk_securities.csv'))
get_prices(symbols, '2014-01-01', datetime.now().strftime('%Y-%m-%d'))
