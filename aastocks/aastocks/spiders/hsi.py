# -*- coding: utf-8 -*-
import os
import logging
import scrapy
import pandas as pd

from aastocks import utils


logger = logging.getLogger(__name__)


class HsiSpider(scrapy.Spider):
    name = 'hsi'
    allowed_domains = ['aastocks.com']
    start_urls = [
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=GEM&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSP&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSHKLI&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSCCI&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSF&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSC&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSHKMI&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSCEI&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSU&t=1&s=&o=1&p=',
        'http://www.aastocks.com/en/stocks/market/index/hk-index-con.aspx?index=HSHKSI&t=1&s=&o=1&p=',
    ]

    def parse(self, response):
        index_abbr = response.css('div.tabTS div#cp_ucTabSystem_pHeader b::text').get()
        index_name = response.css('div.tabS2 h1.newsHeader::text').get().split('-')[-1].strip()

        html = response.css('table#tbTS').get()
        df = utils.stock_htmltable_to_df(html)
        df['IndexAbbreviation'] = index_abbr
        df['IndexName'] = index_name

        os.makedirs('data/hsi', exist_ok=True)
        df[['Symbol', 'Name', 'IndexAbbreviation', 'IndexName']].to_csv('data/hsi/%s.csv' % index_abbr, index=False)
