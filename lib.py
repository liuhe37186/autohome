#!/usr/bin/env python
# encoding: utf-8

def get_cars(brand_name, start_url):
    print('start_url', start_url)
    from setting import headers, wait_sec, domain
    from bs4 import BeautifulSoup
    import requests
    import time
    cars = []
    # 设置referer
    headers['referer'] = start_url

    # 设置起始抓取页面
    now_url = start_url
    # next_url 为空是结束抓取，返回数据的条件
    next_url = ''
    while True:
        result = requests.get(now_url, headers=headers)
        print("origin"+result.encoding,"apparent_encoding"+result.apparent_encoding)
        # result.encoding = result.apparent_encoding
        # print("result:"+result.text)
        print(result.request.headers)
        # result.text = result.text.decode('gb2312').encode('utf-8')
        html_content = result.content
        # print("html_content:",html_content)
        # html_content = html_content.decode('gbk').encode('utf-8')
        # result.encoding="gb2312"
        html_content_soup = BeautifulSoup(html_content, 'html.parser',from_encoding='gb18030')
       
        # html_content_soup.encode("UTF-8")
        # print("origin_encoding",html_content_soup.origin_encoding)
        # print("html:"+html_content_soup.prettify())
        cars_tag = html_content_soup.find_all(class_='list-cont-bg')
        # 结束逻辑
        # 1. 一开始就没有翻页
        # 2. 唯一获取 page-item-next
        # 3. 循环

        if html_content_soup.find(class_="price-page") is None:
            next_url = ''
        else:
            next_url_tag = html_content_soup.find(class_="price-page").find(class_="page-item-next")
            # 结束翻页
            if next_url_tag['href'] == 'javascript:void(0)':
                next_url = ''
            else:
                next_url = domain + next_url_tag['href']
        print ('next_url is ', next_url)
        for car_tag in cars_tag:
            car = {}
            car['brand'] = brand_name
            car['url'] = now_url
            name = car_tag.find(class_='main-title').get_text()
            # print("car_tag:"+car_tag)
            print("main-title:"+car_tag.find(class_='main-title').get_text())
            # newName = name.encode('gb2312')
            # print(newName)
            print(name)
            car['name'] = name
            car['price'] = car_tag.find(class_='font-arial').get_text(strip=True)
        
            for car_attr_tag  in car_tag.find('ul', class_='lever-ul').find_all('li'):
                car_attr = car_attr_tag.get_text(',',strip=True)
                if len(car_attr.split(u'：')) < 2 :
                    continue
                car_attr_key = car_attr.split(u'：')[0]
                car_attr_value = car_attr.split(u'：')[1]
                # 直接空格无效，因为gbk无法转换'\xa0'字符(http://www.educity.cn/wenda/350839.html)
                # car_attr_key = car_attr_key.replace(u'\xa0', '')
                car[car_attr_key] = car_attr_value.strip(',')
            cars.append(car)
        time.sleep(wait_sec)
        # 抓取结束，返回数据
        if next_url == '':
            return cars

        # 更换页面
        now_url = next_url
