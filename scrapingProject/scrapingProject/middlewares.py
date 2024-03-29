# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import logging
from fake_useragent import UserAgent
from scrapingProject.utilities.toripchanger import TorIpChanger

logger = logging.getLogger(__name__)


class RandomUserAgentMiddleware(object):
    """
    This middleware change the user agent for each request or for every time the
    Ip changed
    """
    
    
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        fallback = crawler.settings.get('FAKEUSERAGENT_FALLBACK', None)
        self.ua = UserAgent(fallback=fallback)
        self.per_ip = crawler.settings.get('RANDOM_UA_PER_IP', True)
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
        self.ip2ua = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)
        
        if self.per_ip:
            ip = spider.current_ip
            if ip is None:
                ip = "127.0.0.1"
            if ip not in self.ip2ua:
                self.ip2ua[ip] = get_ua()
                logger.debug('Assign User-Agent %s to ip %s'
                             % (self.ip2ua[ip], ip))
            request.headers.setdefault('User-Agent', self.ip2ua[ip])
        else:
            request.headers.setdefault('User-Agent', get_ua())

class ProxyMiddleware(object):
    """
    Adds a metatag proxy to each request that need to be sent (for the ip proxy)
    and update ip if necessary, depends on ip_changer
    Need privoxy and tor running
    """
    
    ip_changer = TorIpChanger(reuse_threshold=30, number_of_requests_per_ip=200)
    
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        current_ip = self.ip_changer.update_ip()
        if not (current_ip is None):
            spider.current_ip = current_ip

class ScrapingprojectSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        


class ScrapingprojectDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
