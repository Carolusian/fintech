import pandas as pd


def stock_htmltable_to_df(html):
    df = pd.read_html(html)[0]
    df.columns = df.columns.str.replace('▼', '')
    df.columns = df.columns.str.replace('▲', '')
    df.columns = df.columns.str.replace(' ', '')

    df['Name/Symbol'] = df['Name/Symbol'].str.partition('.HK').iloc[:,0] + '.HK'
    df[['Name', 'Symbol']] = df['Name/Symbol'].str.rsplit(' ', expand=True, n=1)

    return df

