import scrapy
from quotes_project.items import QuotesScraperItem #made in the previous step

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = QuotesScraperItem()
            item['text'] = ''.join(quote.css('span.text::text').get())
            item['author'] = ''.join(quote.css('span small::text').get())
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)