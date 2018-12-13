#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Xiaofei Zeng
# Email: xiaofei_zeng@whu.edu.cn
# Created Time: 2018-12-13 11:50

from __future__ import print_function
import sys

from scrapy.spiders import Spider
from scrapy import Request

reload(sys)
sys.setdefaultencoding('utf-8')

class LetpubSpider(Spider):
    name = 'letpub'
    allowed_domains = ['letpub.com.cn']
    start_urls = [
            'http://www.letpub.com.cn/index.php?page=journalapp&fieldtag=&firstletter=&currentpage=1']
    
    def parse(self, response):
        self.f = open('letpub.xls', 'w')
        self.f.write(
                'ISSN\t期刊名\t影响因子\t中科院分区\t'
                '大类学科\t小类学科\tSCI/SCIE\t是否OA\t'
                '录用比例\t审稿周期\t近期文章\t热度(浏览量)\n')
        for i in xrange(1, 1025):
            url = 'http://www.letpub.com.cn/index.php?page=journalapp&fieldtag=&firstletter=&currentpage={0}'.format(i)
            yield Request(url, callback=self.get_table)

    def get_table(self, response):
        for n, sel in enumerate(response.xpath(
                '//tr/td[@style="border:1px #DDD solid; '
                'border-collapse:collapse; '
                'text-align:left; '
                'padding:8px 8px 8px 8px;"]')):
            if n % 12 == 0:
                issn = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 1:
                name = sel.xpath('a/text()').extract()[0] if sel.xpath('a/text()').extract() else 'NULL'
            if n % 12 == 2:
                ifactor = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 3:
                section = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 4:
                big = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 5:
                small = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 6:
                sci = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 7:
                oa = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 8:
                perct = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 9:
                period = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
            if n % 12 == 10:
                recent = 'http://letpub.com.cn/' + sel.xpath('a/@href').extract()[0][1:] if sel.xpath('a/@href').extract() else 'NULL'
            if n % 12 == 11:
                views = sel.xpath('text()').extract()[0] if sel.xpath('text()').extract() else 'NULL'
                self.f.write('\t'.join([
                    issn, name, ifactor, section, 
                    big, small, sci, oa, perct, 
                    period, recent, views])+'\n')
