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
				car = {}
				if child.name == 'dt':
					land = child.get_text();
				else:
					car['brandName'] = brand_name
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
					car['carType'] = get_car_type(car['href'])
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
def get_car_type(series_url):
	# url='https://car.autohome.com.cn/price/series-4851.html'
	res= requests.get(series_url,headers=headers)
	soup = BeautifulSoup(res.content,'html5lib')
    # print(soup.prettify())
	car_details = soup.find(id='divSeries')
	car_type_list = []
	
	engine = ''
    # print(car_details.prettify())

	for tag in car_details.children:

		if isinstance(tag.find('ul'),bs4.element.Tag):
			for li in tag.find('ul').find_all('li'):
				car_type={}
				car_type['车型'] = li.find('div',class_='interval01-list-cars').p.get_text()
				# print(li.find('div',class_='interval01-list-cars').prettify())
					# print(li.find('div',class_='interval01-list-cars').find('span',class_='interval01-list-cars-text').get_text())
				# print(li.find('div',class_='interval01-list-cars').p.get_text())
				for p in li.find('div',class_='interval01-list-cars').find_all('p'):
					spanList=[]
					spanStr={}
					if p.span != None:
						for span in p.children: 
							spanList.append(span.get_text())
                        # print(spanList)
							car_type['配置'] = spanList
						

                # print(li.find('div',class_='interval01-list-cars').p.next_slibing)
                # if li.find('div',class_='interval01-list-cars').p.span != None:
                    # print(li.find('div',class_='interval01-list-cars').p.span.get_text())
				car_type['指导价']= li.find('div',class_='interval01-list-guidance').get_text()
				# print(li.find('div',class_='interval01-list-guidance').get_text())
				# print(car_type)
				# print(car_type)
				car_type_list.append(car_type)
				# print(car_type_list)
	# print(car_type_list)
	return car_type_list












