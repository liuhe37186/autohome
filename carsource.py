#!/usr/bin/env python
# encoding: utf-8
# 根据车辆品牌id查询车系信息

def get_car(brand_name,brand_id):
	from setting import headers, wait_sec, domain,brand_url
	from bs4 import BeautifulSoup
	import requests
	import time
	cars = []
	now_url = brand_url+brand_id

	print(now_url)
	result = requests.get(now_url, headers=headers)
	soup = BeautifulSoup(result.content,'html5lib')
	land = ''
	for dl in soup('dl'):
		# print(dl.prettify())
		for child in dl.children:
			# print(child.prettify())

			car = {}

			if child.name == 'dt':
				land = child.get_text();
			else:
				car['land'] = land
				car['series'] = child.a.get_text().split(" ")[0]
				car['href'] = child.a.attrs['href']
			print(car)


	# soup.prettify()

	# print(soup.prettify())
	