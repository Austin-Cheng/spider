#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/23
import scrapy


class CcgpBeijingItem(scrapy.Item):
    bid_title = scrapy.Field()
    bid_date = scrapy.Field()
    bid_id = scrapy.Field()
    bid_content = scrapy.Field()
    bid_level = scrapy.Field()


class CcgpTianjinItem(scrapy.Item):
    bid_title = scrapy.Field()
    bid_date = scrapy.Field()
    bid_id = scrapy.Field()
    bid_content = scrapy.Field()
    bid_level = scrapy.Field()
    bid_ver = scrapy.Field()







