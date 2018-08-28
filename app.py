#!/usr/bin/env python
# encoding: utf-8
# from lib import get_cars
import requests
from bs4 import BeautifulSoup
from carsource import get_car,get_car_type
from setting import headers, domain, start_url, file_output
import json
import bs4

# output_file = open(file_output, 'w+',encoding='utf-8')

# 第一步提取 品牌列表
# 第二部通过品牌列表提取 车辆详细列表(下一页)

result = requests.get(start_url, headers=headers)

html_content = result.content
html_content_soup = BeautifulSoup(html_content,'html5lib')
brands_tag =  html_content_soup.find_all('li')


def main():
    # url='https://car.autohome.com.cn/price/series-4851.html'
    # get_car_type(url)
    for brand_tag in brands_tag:
    
        car = {}
        brand_name  = brand_tag.get_text(',').split(',')[0]
        brand_id = brand_tag.get('id')[1:]
        brand_href = domain + brand_tag.a['href']
        # print(brand_name,brand_id,brand_href)
        get_car(brand_name, brand_id)

main()

def test():
    url='https://car.autohome.com.cn/price/series-4851.html'
    url_1 = 'https://car.autohome.com.cn/price/series-3170-0-3-0-0-0-0-1.html'
    get_car_type(url_1)

# test()