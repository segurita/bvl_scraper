# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request

from bvl_scraper.items import NemonicoScraperItem


class NemonicosSpider(scrapy.Spider):
    name = "nemonicos"
    allowed_domains = ["bvl.com.pe"]

    def start_requests(self):
        for i in range(65, 91):
            letter = chr(i).lower()
            url = "http://www.bvl.com.pe/includes/empresas_{}.dat".format(letter)
            yield Request(
                url,
                callback=self.scrape_company_page,
            )

    def scrape_company_page(self, response):
        company_links = response.xpath("//td/a/@href").extract()
        for link in company_links:
            url = "http://www.bvl.com.pe{}".format(link)
            yield Request(
                url,
                callback=self.parse,
            )

    def parse(self, response):
        for link in response.xpath("//a/@href").extract():
            res = re.search("Nemonico=(.+)&", link)
            if res:
                nemonico = res.groups()[0]
                item = NemonicoScraperItem()
                item['nemonico'] = nemonico
                yield item
