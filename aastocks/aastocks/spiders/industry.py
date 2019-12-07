# -*- coding: utf-8 -*-
import os
import scrapy
import logging
import pandas as pd
from urllib.parse import urlparse, parse_qs

from aastocks import utils


logger = logging.getLogger(__name__)


class IndustrySpider(scrapy.Spider):
    name = 'industry'
    allowed_domains = ['aastocks.com']
    start_urls = ['http://www.aastocks.com/en/stocks/market/industry/industry-performance.aspx']

    def parse(self, response):
        for link in response.css('table.indview_tbl tr.indview_tr td.colFirst a.a15'): 
            url = link.xpath('@href').get().replace(' ', '')
            yield scrapy.Request('http://www.aastocks.com%s' % url, callback=self.parse_industry)
        
    def parse_industry(self, response):
        parsed = urlparse(response.url)
        industry_symbol = parse_qs(parsed.query)['industrysymbol'][0]
        industry_name = response.css('div.tabS2 h1.newsHeader::text').get().split('-')[-1].strip()
        sector_name = response.css('div.tabS2 h1.newsHeader::text').get().split('-')[-2].strip()

        html = response.css('table#tbTS').get()
        df = utils.stock_htmltable_to_df(html)
        df['IndustrySymbol'] = industry_symbol
        df['Industry'] = industry_name
        df['Sector'] = sector_name

        os.makedirs('data/industry', exist_ok=True)
        df[['Symbol', 'Name', 'IndustrySymbol', 'Industry', 'Sector']].to_csv('data/industry/%s.csv' % industry_symbol)
