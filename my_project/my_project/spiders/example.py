import scrapy
from scrapy.item import Field, Item

class ProductItem(Item):
    name = Field()
    price = Field()


class AmazonSpider(scrapy.Spider):
    name = 'gumtree'
    allowed_domains = ['www.gumtree.com']
    start_urls = [
        'https://www.gumtree.com/flats-houses/property-for-sale',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        },
    }



    def parse(self, response):
        for product in response.xpath(".//div[@class='css-1u9dcvg']"):
            yield {
                "title": product.xpath(".//div[@class='css-1de61eh e25keea13']/text()").get(),
                "price": product.xpath(".//div[@class='css-1ygzid9']/text()").get(),
                "location": product.xpath(".//div[@data-q='tile-location'][@class='css-30gart']").get(),
                "posted_date": product.xpath(".//div[@class='css-ntw5lf']").get()
            }

        next_page_url = response.urljoin('uk/page{}'.format(page_number + 1))
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)