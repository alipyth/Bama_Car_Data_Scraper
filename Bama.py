import scrapy
from scrapy.crawler import CrawlerProcess
import time
SCROLL_RANGE = 3
class QuotesSpider(scrapy.Spider):
    name = 'bama'
    start_urls = ['https://bama.ir/car/samand/all-models/all-trims?hasprice=true']
    def parse(self , response):
        for quote in response.css('.search-new-page'):
            
            yield {
                'name': quote.css('div.title > a > span ::text').extract_first().strip().replace('،', '').encode('utf-8'),
                'model' : quote.css('#adlist > ul > li:nth-child(1) > div.list-data-new-outer > div > div.right-side > div.title > a > span > span:nth-child(2)::text').extract_first().strip().replace('،', '').encode('utf-8'),
                'karkard': quote.css('#adlist > ul > li:nth-child(1) > div.list-data-new-outer > div > div.right-side > div.car-func-details > span:nth-child(1)::text').extract_first().strip().replace('کارکرد', '').replace(',', '').encode('utf-8'),
                'price': quote.css('#adlist > ul > li:nth-child(2) > div.list-data-new-outer > div > div.left-side > p > span:nth-child(1)::text').extract_first().strip().replace(',', '').encode('utf-8'),
                'url': quote.css('a.cartitle::attr("href")').extract_first(),
            }

        next_page = response.css('.paging-new .car-ad-list.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "bama.csv": {"format": "csv"},
        }
    })


process.crawl(QuotesSpider)
process.start() # the script will block here until the crawling is finished
