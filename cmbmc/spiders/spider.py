import scrapy

from scrapy.loader import ItemLoader
from ..items import CmbmcItem
from itemloaders.processors import TakeFirst


class CmbmcSpider(scrapy.Spider):
	name = 'cmbmc'
	start_urls = ['https://www.cmb.mc/en/our-latest-news/']

	def parse(self, response):
		post_links = response.xpath('//a[text()="Read more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="title"]/text()').get()
		description = response.xpath('//div[@class="text-grid-content"]//text()[normalize-space() and not(ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="date-actualite"]/h6[@class="txt-info"]/text()').get()

		item = ItemLoader(item=CmbmcItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
