# -*- coding: utf-8 -*-
from datetime import datetime
import json

import scrapy
from scrapy.http import Request

from bvl_scraper.items import PriceScraperItem


class PricesSpider(scrapy.Spider):
    name = "prices"
    allowed_domains = ["bvl.com.pe"]
    today = datetime.today().strftime("%Y%m%d")
    with open("nemonicos.json", "r") as handle:
        nemonicos = json.loads(handle.read())

    def start_requests(self):
        for nemonico in self.nemonicos:
            url = "http://www.bvl.com.pe/jsp/cotizacion.jsp?fec_inicio=20160101&fec_fin={}&nemonico={}".format(
                self.today,
                nemonico['nemonico'],
            )
            yield Request(
                url,
                meta={'nemonico': nemonico},
                callback=self.parse,
            )

    def parse(self, response):
        for tr in response.xpath("//tr"):
            cells = tr.xpath(".//td")
            if cells:
                price_date = cells[0].xpath("text()").extract_first().strip()
                closing_price = cells[2].xpath("text()").extract_first().strip()
                item = PriceScraperItem()
                item['price_date'] = price_date
                item['closing_price'] = closing_price
                item['nemonico'] = response.meta['nemonico']
                yield item
