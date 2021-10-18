import scrapy

class Tarantula(scrapy.Spider):
    name = "oddsportal"

    def start_requests(self):
        urls = [
            "https://www.oddsportal.com/soccer/england/premier-league-2008-2009/results/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = './test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
