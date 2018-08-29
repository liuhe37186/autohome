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


					res= requests.get(car['href'],headers=headers)
					soup1 = BeautifulSoup(res.content,'html5lib')

					tab = soup1.find('div',class_='tab-nav border-t-no')

					if isinstance(tab.find('ul'),bs4.element.Tag):
						for li in tab.find('ul').find_all('li'):
							if li.a != None:
								print(li.a.get('href'))
								print(li.a.get_text())
								carStatus = li.a.get_text()
								carUrl = domain+li.a.get('href')							
								car[carStatus] = get_car_type(carUrl)
								cars.append(car)
					line = json.dumps(car, indent=2,ensure_ascii=False)

					print(line+'\n')
					# # 输出 Unicode 到文件
  
					output_file.write(line)
					output_file.write(',\n')
					# car_all = get_car_detail(car['href'],car)
					# return car_all
					# print(cars)
					

def get_car_status(series_url):
	res= requests.get(series_url,headers=headers)
	soup = BeautifulSoup(res.content,'html5lib')

	tab = soup.find('div',class_='tab-nav border-t-no')

	if isinstance(tab.find('ul'),bs4.element.Tag):
		for li in tab.find('ul').find_all('li'):
			print(li.a.get('href'))
			print(li.a.get_text())
			carStatus = li.a.get_text
			carUrl = li.a.get('href')


	# soup.prettify()
def get_car_type(series_url):

	now_url = series_url
    # next_url 为空是结束抓取，返回数据的条件
	next_url = ''
	car_type_list = []
	while True:

		# url='https://car.autohome.com.cn/price/series-4851.html'
		res= requests.get(now_url,headers=headers)
		soup = BeautifulSoup(res.content,'html5lib')
		# print(soup.prettify())
		engine = ''
	    # print(car_details.prettify())
		if soup.find(class_="price-page02") is None:
			next_url = ''
		else:
			next_url_tag = soup.find(class_="price-page02").find(class_="page-item-next")
			# 结束翻页
			if next_url_tag['href'] == 'javascript:void(0)':
				next_url = ''
			else:
				next_url = domain + next_url_tag['href']
				print('next_url',next_url)
		car_details = soup.find(id='divSeries')
		for tag in car_details.children:
			# print(tag.find('div',class_='interval01-list-cars').prettify())
			# print(tag)
			
			engine=''
			if isinstance(tag,bs4.element.Tag):
				# print(tag.prettify())
				# print(tag.find('span',class_='interval01-list-cars-text').get_text())
				engine = tag.find('span',class_='interval01-list-cars-text').get_text()
				


			if isinstance(tag.find('ul'),bs4.element.Tag):
				for li in tag.find('ul').find_all('li'):

					if isinstance(li.find('div',class_='interval01-list-cars'),bs4.element.Tag):
						for div in li.find('div',class_='interval01-list-cars').children:
							car_type={}
							car_type['类别'] = engine
							car_type['车型'] = li.find('div',class_='interval01-list-cars').p.get_text()
							# print(li.find('div',class_='interval01-list-cars').prettify())
							# print(li.find('div',class_='interval01-list-cars').find('span',class_='interval01-list-cars-text').get_text())
						# print(li.find('div',class_='interval01-list-cars').p.get_text())
						# print(li.prettify())
							for p in div.find_all('p'):
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
		print(car_type_list)
		# return car_type_list
	        # 抓取结束，返回数据
		if next_url == '':
			return car_type_list

	        # 更换页面
		now_url = next_url











