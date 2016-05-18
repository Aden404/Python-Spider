# -*- coding: utf-8 -*-
import scrapy
import re
from  Movie_100.items import Movie100Item

class Movie100BySpider(scrapy.Spider):
    name = "Movie_100_BY"
    #allowed_domains = ["www.douban.com/doulist/42564/"]
    start_urls = (
        'https://www.douban.com/doulist/42564/?start=0&sort=time&sub_type=',
    )
    def parse(self, response):
        #print (response.body)
        item = Movie100Item()
        selector =  scrapy.Selector(response)
        movies = selector.xpath('//div[@class="bd doulist-subject"]')
        for each in movies:
            title = each.xpath('div[@class="title"]/a/text()').extract()[0]
            rate = each.xpath('div[@class="rating"]/span[@class="rating_nums"]/text()').extract()[0]
            director = re.search('<div class="abstract">(.*?)<br',each.extract(),re.S).group(1)
            title = title.replace(' ', '').replace('\n', '')
            director = director.replace(' ', '').replace('\n', '')
            #mes = re.search('<br />(.*?)</div>',each.extract(),re.S).
            #type = re.search('<div class="abstract">(.*?)<br />(.*?)<br />(.*?)<br />', each.extract(), re.S).group(2)
            #country = re.search('<div class="abstract">(.*?)<br />(.*?)<br />(.*?)<br />', each.extract(), re.S).group(3)
            item['title'] = title
            item['rate'] = rate
            item['director'] = director
            #print "title: " + title
            #print "rate: " + rate
            #print  director
            yield item
            nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
            if nextPage:
                next = nextPage[0]
                print next
                yield scrapy.http.Request(next, callback=self.parse)

