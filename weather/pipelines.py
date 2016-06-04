# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
from spiders.bloom import BloomFilter

class WeatherPipeline(object):
  def __init__(self):
    self._bf = BloomFilter(0.0001,100000)
    self._count = 0
    
  def process_item(self, item, spider):
    with open('data.txt','a') as file:
      if item['city'] and item['temp'] and not self._bf.is_element_exist(item['city'].encode('utf-8')):
        self._bf.insert_element(item['city'].encode('utf-8'))
        self._count+=1
        entry = "%d  %s  %s  %s  %s  %s  %s\n"%(self._count,item['city'].encode('utf-8'),item['temp'].encode('utf-8'),item['wuran'].encode('utf-8'),item['qihou'].encode('utf-8'),item['wind'].encode('utf-8'),item['shidu'].encode('utf-8'))
        file.write(entry)
      file.close()
    return item
