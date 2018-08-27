#!/usr/bin/env python
# encoding: utf-8
# 根据车辆品牌id查询车系信息
from setting import headers, wait_sec, domain,brand_url
from bs4 import BeautifulSoup
import requests
import time
import bs4
from setting import headers, domain, start_url, file_output
import json
cars = []
car = {}
output_file = open(file_output, 'w+',encoding='utf-8')
def get_car(brand_name,brand_id):
	
	
	now_url = brand_url+brand_id

	print(now_url)
	result = requests.get(now_url, headers=headers)
	soup = BeautifulSoup(result.content,'html5lib')
	land = ''
	
	for dl in soup('dl'):
		# print(dl.prettify())
		for child in dl.children:
			# print(child.prettify())
		
			if isinstance(child,bs4.element.Tag):
				if child.name == 'dt':
					land = child.get_text();
				else:
					car['brand_name'] = brand_name
					car['land'] = land
					car['series'] = child.a.get_text()
					car['href'] = domain+child.a.attrs['href']
					result = requests.get(car['href'],headers=headers)
					soup = BeautifulSoup(result.content,'html5lib')
					car_details = soup.find(class_='list-cont-main')
					car['price'] = car_details.find(class_='font-arial').get_text(strip=True)
					for car_attr_tag  in car_details.find('ul', class_='lever-ul').find_all('li'):
						car_attr = car_attr_tag.get_text(',',strip=True)
						if len(car_attr.split(u'：')) < 2 :
							continue
						car_attr_key = car_attr.split(u'：')[0]
						car_attr_value = car_attr.split(u'：')[1]
                		# 直接空格无效，因为gbk无法转换'\xa0'字符(http://www.educity.cn/wenda/350839.html)
						car_attr_key = car_attr_key.replace(u'\xa0', '')
						car[car_attr_key] = car_attr_value.strip(',')
						cars.append(car)
						line = json.dumps(car, indent=2,ensure_ascii=False)

						print(line+'\n')
						# 输出 Unicode 到文件
  
						output_file.write(line)
						output_file.write('\n')
					# car_all = get_car_detail(car['href'],car)
					# return car_all
					# print(cars)
					

	# soup.prettify()

	# print(soup.prettify())
def get_car_detail(car_detail_url,car):

	result = requests.get(car_detail_url,headers=headers)
	soup = BeautifulSoup(result.content,'html5lib')
	car_details = soup.find(class_='list-cont-main')
	car['price'] = car_details.find(class_='font-arial').get_text(strip=True)
	for car_attr_tag  in car_details.find('ul', class_='lever-ul').find_all('li'):
		car_attr = car_attr_tag.get_text(',',strip=True)
		if len(car_attr.split(u'：')) < 2 :
			continue
		car_attr_key = car_attr.split(u'：')[0]
		car_attr_value = car_attr.split(u'：')[1]
                # 直接空格无效，因为gbk无法转换'\xa0'字符(http://www.educity.cn/wenda/350839.html)
		car_attr_key = car_attr_key.replace(u'\xa0', '')
		car[car_attr_key] = car_attr_value.strip(',')
		print(car)
		# return car
	# print(car)
	
	
	# for tag in car_details.children:
		# car['级别']=tag.find(class_='info-gray').get_text()
		# print(car)
		# tag.prettify()
		# print(tag.find_all('li'))

	# print(car_details.prettify())












