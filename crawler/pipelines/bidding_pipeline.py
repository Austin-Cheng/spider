#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/23
import scrapy
import json
import codecs


class CcgpBeijingPipeline:
    def open_spider(self, file_name):
        self.file_attrs = codecs.open('data/ccgp/beijing/attributes.json', 'a+', encoding='utf-8')

    def _open_spider(self, file_name):
        self.file_content = codecs.open('data/ccgp/beijing/%s.html' % file_name, 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file_attrs.close()

    def _close_spider(self):
        self.file_content.close()

    def process_item(self, item, spider):
        item['bid_id'] = item['bid_id'][2:-5].replace('/', '_')
        self._open_spider(item['bid_id'])
        attrs_dict = {
            'bid_id': item['bid_id'],
            'bid_level': item['bid_level'],
            'bid_date': item['bid_date'],
            'bid_title': item['bid_title']
        }
        attrs_json = json.dumps(attrs_dict, ensure_ascii=False) + "\n"
        self.file_content.write(item['bid_content'])
        self.file_attrs.write(attrs_json)
        self._close_spider()
        return item


class CcgpTianjinPipeline:
    def open_spider(self, file_name):
        self.file_attrs = codecs.open('data/ccgp/tianjin/attributes.json', 'a+', encoding='utf-8')

    def _open_spider(self, file_name):
        self.file_content = codecs.open('data/ccgp/tianjin/%s.html' % file_name, 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file_attrs.close()

    def _close_spider(self):
        self.file_content.close()

    def process_item(self, item, spider):
        item['bid_id'] = item['bid_id']
        self._open_spider(item['bid_id'])
        attrs_dict = {
            'bid_id': item['bid_id'],
            'bid_level': item['bid_level'],
            'bid_date': item['bid_date'],
            'bid_title': item['bid_title'],
            'bid_ver': item['bid_ver']
        }
        attrs_json = json.dumps(attrs_dict, ensure_ascii=False) + "\n"
        self.file_content.write(item['bid_content'])
        self.file_attrs.write(attrs_json)
        self._close_spider()
        return item