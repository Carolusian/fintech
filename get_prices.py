import os
import pandas as pd
import threading
import yfinance as yf
from datetime import datetime
from yahoofinancials import YahooFinancials


def get_hk_stock_symbols(file_path):
    df = pd.read_csv(file_path, skiprows=2, dtype = {'Stock Code': str})
    df = df[df['Category'] == 'Equity']
    df['sym'] = df['Stock Code'].str.extract('(?P<digital>[\d]{4}$)', expand=False)
    df['sym'] = df['sym'].astype(str) + '.HK'
    return df['sym'].tolist()


def create_dirs(dir):
    home_dir = os.path.expanduser('~')
    main_dir = os.path.join(home_dir, 'stock-data', dir)
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
    return main_dir

class StockData(threading.Thread):
    def __init__(self, sym):
        self.sym = sym
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.folder_name = 'hk-historical-prices'
        self.financials_folder = 'hk-financials'
        self.summary_folder = 'hk-summary'
        self.statistics_folder = 'hk-statistics'
        self.stock_handler = yf.Ticker(sym)
        self.stock_handler_alt = YahooFinancials(sym)
        threading.Thread.__init__(self)

    def run(self):
        print('# start getting historical prices for %s' % self.sym)
        self.get_prices()

        print('# start getting financial statments for %s' % self.sym)
        self.get_financial_stmts()

        print('# start getting statistics data for %s' % self.sym)
        self.get_stats()

        print('# start getting summary data for %s' % self.sym)
        self.get_summary()

    def get_prices(self):
        cache_dir = create_dirs(self.folder_name)
        summary_folder = create_dirs(self.summary_folder)
        statistics_folder = create_dirs(self.statistics_folder)

        try:
            data = self.stock_handler.history(period='max')
            df = pd.DataFrame.from_dict(data)
            df.to_csv(os.path.join(cache_dir, self.sym + '.csv'))
            return self.sym, data
        except Exception:
            print('# Error in downloading {}'.format(self.sym))
            return None


    def get_financial_stmts(self):
        financials_dir = create_dirs(self.financials_folder)
        balance_sheet = self.stock_handler.balance_sheet
        cashflow = self.stock_handler.cashflow
        income_stmts = self.stock_handler.financials

        financials = (pd.concat([income_stmts, balance_sheet, cashflow])
                        .transpose()
                        .assign(Date = lambda x: x.index)
                        .sort_index())
        financials.columns = financials.columns.str.replace(' ', '')
        cols = list(financials.columns)
        financials[[cols[-1]] + cols[:-1]].to_csv(os.path.join(financials_dir, self.sym + '.csv'), index=False)


    def get_stats(self):
        stats_dir = create_dirs(self.statistics_folder)
        stats = self.stock_handler_alt.get_key_statistics_data()
        df_stats = (pd.DataFrame
                .from_dict(stats)
                .transpose()
                .assign(Symbol = lambda x: x.index))
        cols = list(df_stats.columns)
        df_stats[[cols[-1]] + cols[:-1]].to_csv(os.path.join(stats_dir, self.sym + '.csv'), index=False)


    def get_summary(self):
        summary_dir = create_dirs(self.summary_folder)
        summary = self.stock_handler_alt.get_summary_data()
        df_summary = (pd.DataFrame
                .from_dict(summary)
                .transpose()
                .assign(Symbol = lambda x: x.index))
        cols = list(df_summary.columns)
        df_summary[[cols[-1]] + cols[:-1]].to_csv(os.path.join(summary_dir, self.sym + '.csv'), index=False)


symbols = get_hk_stock_symbols(os.path.join(os.getcwd(), '2019-12-03_FullListOfSecuritiesHK.csv'))

# Break symbols in buckets in size of 10 each
# Then download stockdata with multi-threading
for i in range(0, 10, 10):
    threads = []
    end = i + 10 if i + 10 < len(symbols) else len(symbols)
    
    for j in range(i, end):
        thread = StockData(symbols[j])
        thread.start()
        threads.append(thread)
 
    for t in threads:
        t.join()
