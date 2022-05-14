import scrapy

#setting the limit of pages before 100
page_limit = True


class Link(scrapy.Item):
    link = scrapy.Field()

#creating the class Spider for scapry
class placesSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['http://www.films101.com']
    try:
        with open("../../link_lists.csv", "rt") as f:
            #starting to execute the links from csv starting from 1 because of heading
            start_urls = [url.strip() for url in f.readlines()][1:]
            if page_limit:
                start_urls = start_urls[0:101]
    except:
        start_urls = []

    #get the list of places for every year on the website
    #starting from first place(country), we dont count all places
    def parse(self, response):
        print(response)
        xpath = '//td[@class="zt1"]/a/@href'
        selection = response.xpath(xpath)
        for s in selection[1:]:
            l = Link()
            l['link'] ='http://www.films101.com' + '/' + s.get()
            print(l)
            yield l
            
            
import scrapy


class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'years'
    allowed_domains = ['http://www.films101.com']
    start_urls = ['http://www.films101.com/years.htm']
    
    #get thed list of year urls
    def parse(self, response):
        xpath = '//div[@id="yearbx"]//a/@href'
        year_urls = response.xpath(xpath)
        for y in year_urls:
            l = Link()
            l['link'] = 'http://www.films101.com/' + y.get()
            yield l




import scrapy


page_limit = True


class Table(scrapy.Item):
    movie = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
    country = scrapy.Field()


#creating the class Spider for scapry
class tableSpider(scrapy.Spider):
    name = 'data'
    allowed_domains = ['www.films101.com']
    try:
        with open("../../movies_scrapy.csv", "rt") as f:
            # starting to execute the links from csv starting from 1 because of heading
            start_urls = [url.strip() for url in f.readlines()][1:]
            #setting the limit of pages before 100

    except:
        start_urls = []

    def parse(self, response):
        t = Table()

        movie1 = '//h1/text()'
        year1 = '//a[re:test(@href, "y[0-9]+r")]/text()'
        director1 = '//a[re:test(@href, "d[0-9]+r")]/text()'
        country1 = '//a[re:test(@href, "c[a-z]+r.htm")]/text()'

        t['movie'] = response.xpath(movie1).getall()
        t['year'] = response.xpath(year1).getall()
        t['director'] = response.xpath(director1).getall()
        t['country'] = response.xpath(country1).getall()

        yield t
        