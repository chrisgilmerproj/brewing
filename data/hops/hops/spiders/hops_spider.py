# -*- coding: utf-8 -*-
import scrapy

from hops.items import HopsItem


class HopslistSpider(scrapy.Spider):
    name = "hopslist"
    allowed_domains = ["hopslist.com"]
    start_urls = (
        'http://www.hopslist.com/',
    )

    def parse(self, response):
        for href in response.xpath("//ul[@class='category-module']/li/h6/a/@href").extract():  # nopep8
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_hops_contents)

    def parse_hops_contents(self, response):
        item = HopsItem()

        item['source'] = response.url

        component = response.xpath("//h2[@class='componentheading']/text()").extract()  # nopep8
        item['component'] = component[0].strip()
        name = response.xpath("//h2[@class='contentheading']/text()").extract()
        item['name'] = name[0].strip()
        for entry in response.xpath('//table/tbody/tr'):
            category = entry.xpath('td[1]/text()').extract()
            data = entry.xpath('td[2]/text()').extract()
            cat_safe = ' '.join([c.strip() for c in category]).lower().strip()
            data_safe = ' '.join([d.strip() for d in data])
            if cat_safe:
                cat_safe = cat_safe.replace(' ', '_')
                cat_safe = cat_safe.replace(' ', '-')
                if 'humulone' in cat_safe:
                    cat_safe = 'co_humulone_composition'
                item[cat_safe] = data_safe
        yield item
