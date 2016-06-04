# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  city = scrapy.Field()
  temp = scrapy.Field()
  qihou = scrapy.Field()
  wind = scrapy.Field()
  shidu = scrapy.Field()
  wuran = scrapy.Field()
  ourl = scrapy.Field()
  pass
