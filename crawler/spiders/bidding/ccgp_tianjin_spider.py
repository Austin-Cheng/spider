#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/23
import scrapy
from items.bidding_item import CcgpTianjinItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re


class CcgpTianjinSpider(scrapy.Spider):
    name = "bid_ccgp_tianjin"
    allow_domain = ['ccgp-tianjin.gov.cn']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        # 'LOG_FILE': None,
        'ITEM_PIPELINES': {'pipelines.bidding_pipeline.CcgpTianjinPipeline': 200},
    }

    def start_requests(self):
        start_url = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
        form_data_sj = {
            'page': '1',
            'method': 'view',
            'step': '1',
            'view': 'Infor',
            'st': '1',
            'id': '1665',
            'ldateQGE': '',
            'ldateQLE': ''
        }
        form_data_qj = {
            'page': '1',
            'method': 'view',
            'step': '1',
            'view': 'Infor',
            'id': '1664',
            'ldateQGE': '',
            'ldateQLE': ''
        }
        for page in range(1, 504):
            form_data_sj['page'] = str(page)
            yield scrapy.FormRequest(start_url, formdata=form_data_sj, callback=self.parse_bid_list,
                                     errback=self.error_back, cb_kwargs={'bid_level': '市级'})
        for page in range(1, 1237):
            form_data_qj['page'] = str(page)
            yield scrapy.FormRequest(start_url, formdata=form_data_qj, callback=self.parse_bid_list,
                                     errback=self.error_back, cb_kwargs={'bid_level': '区级'})

    def parse_bid_list(self, response, **cb_kwargs):
        lis = response.xpath('//ul[@class="dataList"]/li')
        for li in lis:
            bid_href = li.xpath('a/@href').extract()[0]
            bid_title = li.xpath('a/text()').extract()[0]
            bid_date = li.xpath('span/text()').extract()[0]
            bid_level = cb_kwargs['bid_level']
            bid_id, bid_ver = self._parse_href(bid_href)
            bid_url = 'http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&id=%s&ver=%s' % (bid_id, bid_ver)
            args = {
                'bid_title': bid_title,
                'bid_date': bid_date,
                'bid_id': bid_id,
                'bid_level': bid_level,
                'bid_ver': bid_ver
            }
            yield scrapy.Request(bid_url, callback=self.parse_bid_detail, cb_kwargs=args, errback=self.error_back)

    @staticmethod
    def _parse_href(href):
        pattern = 'id=(.*?)&ver=(.*?)$'
        res = re.search(pattern, href)
        return res.group(1), res.group(2)

    def parse_bid_detail(self, response, **cb_kwargs):
        print(response.url)
        item = CcgpTianjinItem(cb_kwargs)
        item['bid_content'] = response.text
        yield item

    def error_back(self, failure):
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
