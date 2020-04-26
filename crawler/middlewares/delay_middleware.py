#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/23
import logging
import random
import time


class RandomDelayMiddleware:
    def __init__(self, delay):
        self.delay = delay

    def process_request(self, request, spider):
        delay = random.randint(1, self.delay)
        time.sleep(delay)
        logging.info('random delay %s seconds' % delay)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DOWNLOAD_DELAY', 5))


