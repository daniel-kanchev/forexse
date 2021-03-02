import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from forexse.items import Article


class ForexseSpider(scrapy.Spider):
    name = 'forexse'
    start_urls = ['https://www.forex.se/pressrum']

    def parse(self, response):
        articles = response.xpath('//div[@class="genericcontentblock block block--col12 "]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article.xpath('.//h2//text()').get()
            date = article.xpath('.//p[1]//text()').get()

            content = article.xpath('.//div[@class="content-block__text"]//text()').getall()
            content = [text for text in content if text.strip()]
            content = "\n".join(content[1:]).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()



