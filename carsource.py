#!/usr/bin/env python
# encoding: utf-8
# 根据车辆品牌id查询车系信息

def get_car(brand_id):
	from setting import headers, wait_sec, domain,brand_url
	from bs4 import BeautifulSoup
	import requests
	import time
	cars = []
	now_url = brand_url+brand_id

	print(now_url)
	result = requests.get(now_url, headers=headers)
	soup = BeautifulSoup(result.content,'html5lib')

	# soup.prettify()

	# print(soup.prettify())
	