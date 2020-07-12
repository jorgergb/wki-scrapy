import scrapy
from scrapy.responsetypes import Response
from wikipedia.items import WikipediaItem
from wikipedia.spiders.tokensVocab import lectura, procesamiento, grafica

# scrapy crawl wiki -o wiki.csv


class WikiSpider(scrapy.Spider):

    name = "wiki"
    allowed_domains = ["es.wikipedia.org"]
    start_urls = [
        "https://es.wikipedia.org/wiki/Wikipedia:Portada"
    ]
    path = 'wiki.csv'

    def parse(self, response):

        urls = []
        for href in response.xpath('//div[@id="main-cur"]/ul/li//a/@href').getall():
            url = response.urljoin(href)
            print(url)
            if url not in urls:
                urls.append(url)
                yield scrapy.Request(url, callback=self.parse_page)


    def parse_page(self, response: Response):
        try:
            div = response.xpath('//div[@class="mw-parser-output"]')
            for element in div.xpath('p'):
                item = WikipediaItem()

                contents = element.xpath('string()').get()
                content = contents.encode('utf-8')

                item['topic'] = response
                item['text'] = content

                yield item
        except Exception as e:
            print(e)

    def close(self, reason):
        df = lectura(self.path)
        df = procesamiento(df)
        grafica(df)
