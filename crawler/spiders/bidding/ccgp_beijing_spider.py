#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/23
import scrapy
from items.bidding_item import CcgpBeijingItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class CcgpBeijingSpider(scrapy.Spider):
    name = "bid_ccgp_beijing"
    allow_domain = ['ccgp-beijing.gov.cn']
    start_url1 = 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index.html'
    start_url2 = 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/index.html'
    start_urls = [start_url1, start_url2]
    # total page 143
    for page in range(1, 143):
        url1 = 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_%s.html' % page
        url2 = 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/index_%s.html' % page
        start_urls.append(url1)
        start_urls.append(url2)

    custom_settings = {
        'ITEM_PIPELINES': {'pipelines.bidding_pipeline.CcgpBeijingPipeline': 200},
    }

    def start_requests(self):
        for url in self.start_urls:
            print(url)
            bid_level = '市级' if 'sjzfcggg' in url else '区级'
            yield scrapy.Request(url, callback=self.parse_bid_list, cb_kwargs={'bid_level': bid_level})

    def parse_bid_list(self, response, **cb_kwargs):
        lis = response.xpath('//body//ul[@class="xinxi_ul"]/li')
        for li in lis:
            bid_id = li.xpath('a/@href').extract()[0]
            bid_title = li.xpath('a/text()').extract()[0]
            bid_date = li.xpath('span/text()').extract()[0]
            bid_level = cb_kwargs['bid_level']
            url_arg = 'sjzfcggg' if bid_level == '市级' else 'qjzfcggg'
            bid_url = 'http://www.ccgp-beijing.gov.cn/xxgg/' + url_arg + bid_id[1:]
            args = {
                'bid_title': bid_title,
                'bid_date': bid_date,
                'bid_id': bid_id,
                'bid_level': bid_level
            }
            yield scrapy.Request(bid_url, callback=self.parse_bid_detail, cb_kwargs=args, errback=self.error_back)

    def parse_bid_detail(self, response, **cb_kwargs):
        item = CcgpBeijingItem(cb_kwargs)
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
