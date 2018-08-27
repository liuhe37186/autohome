#!/usr/bin/env python
# encoding: utf-8
# from lib import get_cars
import requests
from bs4 import BeautifulSoup
from carsource import get_car,get_car_detail
from setting import headers, domain, start_url, file_output
import json

# output_file = open(file_output, 'w+',encoding='utf-8')

# 第一步提取 品牌列表
# 第二部通过品牌列表提取 车辆详细列表(下一页)

result = requests.get(start_url, headers=headers)

html_content = result.content
html_content_soup = BeautifulSoup(html_content,'html5lib')
brands_tag =  html_content_soup.find_all('li')
# series_tag = html_content_soup.find_all('a')

# for series in series_tag:

    # print(series.get_text().split('(')[0])
     # print(series.get_text())

def main():
    brand_tag = brands_tag[4]
    cars = []
    brand_name  = brand_tag.get_text(',').split(',')[0]
    brand_id = brand_tag.get('id')[1:]
    brand_href = domain + brand_tag.a['href']
    print(brand_name,brand_id,brand_href)
    get_car(brand_name,brand_id)
    # get_car_detail('https://car.autohome.com.cn/price/series-3170.html')

# main()
for brand_tag in brands_tag:

    # print(brand_tag)
    
    car = {}
    brand_name  = brand_tag.get_text(',').split(',')[0]
    brand_id = brand_tag.get('id')[1:]
    brand_href = domain + brand_tag.a['href']
    print(brand_name,brand_id,brand_href)
    get_car(brand_name, brand_id)
    # print(car)
    # 输出中文问题
    # for car in cars:
    # line = json.dumps(car, indent=2,ensure_ascii=False)

    # print(line+'\n')
    #     # 输出 Unicode 到文件
  
    # output_file.write(line)
    # output_file.write('\n')
      
