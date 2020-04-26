#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Austin
# date: 2020/3/23
import logging
import random


class RandomUserAgentMiddleware:
    def __init__(self, agents):
        self.agents = agents

    def process_request(self, request, spider):
        agent = random.choice(self.agents)
        request.headers.setdefault('User-Agent', agent)
        logging.info('random user-agent: %s' % agent)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
