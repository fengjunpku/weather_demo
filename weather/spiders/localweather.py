# -*- coding: utf-8 -*-
# localweather.py
import scrapy
from bs4 import BeautifulSoup
from weather.items import WeatherItem
from bloom import BloomFilter
import re,sys

#reload(sys)                      # reload 才能调用 setdefaultencoding 方法  
#sys.setdefaultencoding('utf-8')  # 设置 'utf-8'  
class WeatherSpider(scrapy.Spider):
  name = "myweather"
  allowed_domains = ["sina.com.cn"]
  start_urls = ['http://weather.sina.com.cn/beijing']

  def __init__(self):
    self._bf = BloomFilter(0.0001,100000)

  def parse(self, response):
    html_doc = response.body
    #html_doc = html_doc.decode('utf-8')
    self._bf.insert_element(response.url)
    soup = BeautifulSoup(html_doc,'html.parser',from_encoding='utf-8')
    item = WeatherItem()
    item['ourl'] = response.url
    item['city'] = ''
    item['temp'] = ''
    item['qihou'] = ''
    item['wind'] = ''
    item['shidu'] = ''
    item['wuran'] = ''
    soup_city = soup.find(id='slider_ct_name')
    soup_temp = soup.find('div',{'class','slider_degree'})
    soup_xijie = soup.find('p',{'class','slider_detail'})
    soup_wuran = soup.find('div',{'class','slider_warn_i_tt'})
    if soup_city and soup_temp and soup_wuran:
      item['city'] = soup_city.get_text()
      item['temp'] = soup_temp.get_text()
      xijie = soup_xijie.get_text()
      item['wuran'] = soup_wuran.find('p').get_text()
      item['qihou'] = xijie.split('|')[0].strip()
      item['wind'] = xijie.split('|')[1].strip()
      item['shidu'] = xijie.split('|')[2].strip()
      item['shidu'] = item['shidu'].split(u'：')[1]
    urls_tmp = soup.find_all('a')
    urls = []
    for url_tmp in urls_tmp:
      urls.append(url_tmp.get('href'))
    yield item
    for url in self._cut_urls(urls):
      yield self.make_requests_from_url(url)
  
  def _cut_urls(self,urls):
    cut_urls=[]
    pattern = re.compile(r'http://weather.sina.com.cn/')
    for url in urls:
      try:
        match = pattern.match(url)
      except TypeError as e:
        match = False
      if match and not self._bf.is_element_exist(url):
        cut_urls.append(url)
    return cut_urls
