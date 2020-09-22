# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wxapp.items import WxappItem
from scrapy.http.request

class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'),
             follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),callback="parse_detail",
             follow=False),
    )

    def parse_detail(self, response):
        print("\033[0;37;40m\t=============URL===============\033[0m")
        print("\033[0;37;40m\t" + response.request.url + "\033[0m")

        title = response.xpath("//div[@class='h hm cl']/div[@class='cl']/h1/text()").get().strip()
        author = response.xpath("//div[@class='avatar_right cl']//p[@class='authors']/a/text()").get().strip()
        time = response.xpath("//div[@class='avatar_right cl']//p[@class='authors']/span/text()").get().strip()
        content = response.xpath("//div[@class='content_middle cl']/div[@class='d']/table//td[@id='article_content']//text()").getall()
        content = "".join(content).strip()
        item = WxappItem(title=title,author=author,time=time,content=content)
        yield item
