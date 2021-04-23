import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import AibItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class AibSpider(scrapy.Spider):
	name = 'aib'
	start_urls = ['https://www.aib.af/aibpublic/about_newsroom']

	def parse(self, response):
		articles = response.xpath('//div[contains(@class,"aib_col aib_thr_col aib")]')
		for article in articles:
			date = ''.join(article.xpath('.//div[@class="aib-news-date"]/span/text()').getall())
			post_links = article.xpath('.//a[@title="Find Out More"]/@href').get()
			yield response.follow(post_links, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//section[@class="aib_text_section"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=AibItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
