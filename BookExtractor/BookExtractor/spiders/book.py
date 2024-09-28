import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BookextractorItem


class BookSpider(CrawlSpider):
    name = "book" 



    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    rules = (
        Rule(LinkExtractor(restrict_css='ul[class="nav nav-list"] > li > ul > li > a'),follow=True),
        Rule(LinkExtractor(restrict_css='li[class="next"]'),follow=True),
        Rule(LinkExtractor(restrict_css='article[class="product_pod"] > h3 > a '), callback="parse_item"),
        )
    

    def parse_item(self, response):
        item = BookextractorItem()
        item['image_link'] = response.urljoin(response.css('div[class="item active"] > img').attrib['src'])
        item['title'] = response.css('div[class="col-sm-6 product_main"] > h1::text').get()
        item['price'] = response.css('div.product_main > p.price_color::text').get()
        item['availability'] = response.css('div.product_main > p:nth-child(3)::text').extract()
        item['star'] = response.css('div.product_main p:nth-child(4)::attr(class)').get()
        item['upc'] = response.xpath('//tr[1]//td/text()').get()
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        
        return item
