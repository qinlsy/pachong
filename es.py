import scrapy
from lxml import etree
import json
# import requests
from fontTools.ttLib import TTFont
from fontTools.ttLib import TTFont
from ttest.items import TtestItem
import requests
import time
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import ray

font = TTFont('e:/gzfont.woff2')
font.saveXML('font.xml')
next_url = []

time_start = time.time()  # 记录开始时间

@ray.remote
def getd(b):

    page = f'page={b}'
    urls = 'https://mapi.guazi.com/car-source/carList/pcList?versionId=0.0.0.0&sourceFrom=wap&deviceId=bb8029c5-e216-4f90-8fc6-3b9423b364cc&osv=Windows+10&minor=&sourceType=&ec_buy_car_list_ab=&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&car_color=&guobie=&bright_spot_config=&seat=&fuel_type=&order=&priceRange=0,-1&tag_types=10012&diff_city=&intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&page=1&pageSize=20&city_filter=12&city=12&guazi_city=12&qpres=674754674834669568&platfromSource=wap'
    urls = urls.replace('page=1', page)
    header = {'user-agent': UserAgent().random}
    response = requests.get(url=urls, headers=header)
    text = response.text
    print(text)
    data = json.loads(text)
    data = data['data']
    tol = data['total_desc']
    page = data['totalPage']
    print(f'正在爬取{b}/{page}')
    for j in range(20):
        title = data['postList'][j]['title']
        year = data['postList'][j]['license_date']
        price = data['postList'][j]['price']
        road_haul = data['postList'][j]['road_haul']

        # print(tol,page,'\n',title,'\n',year,'\n',price)
        a = [
            {'id': '&#57808;', 'num': '7'},
            {'id': '&#58149;', 'num': '4'},
            {'id': '&#58397;', 'num': '1'},
            {'id': '&#58585;', 'num': ''},
            {'id': '&#58670;', 'num': '9'},
            {'id': '&#58928;', 'num': '2'},
            {'id': '&#59246;', 'num': '8'},
            {'id': '&#59537;', 'num': '5'},
            {'id': '&#59854;', 'num': '0'},
            {'id': '&#60146;', 'num': '3'},
            {'id': '&#60492;', 'num': '6'},
            {'id': '&#63426;', 'num': ''},
            {'id': '&#63626;', 'num': '7'}]
        # import re
        # cz = re.findall('&.*?;',' &#58397;&#59246;.&#59537;&#60492;万')
        # print(cz)
        for i in a:
            # print(i)
            price = price.replace(i['id'], i['num'])
        # print(price)

        for i in a:
            road_haul = road_haul.replace(i['id'], i['num'])
        # print(road_haul)
        # print(tol,'\n' ,1,'/',page, '\n', title, '\n', year, '\n', price,'\n',road_haul)

        item = {}
        item['title'] = title
        item['year'] = year
        item['price'] = price
        item['road_haul'] = road_haul
        with open('./erdriver.txt', 'a+', encoding='utf-8') as f:
            f.write(json.dumps(item) + '\n')
        print(item)

# 分布式
ray.init(num_cpus=16,ignore_reinit_error=True)


settings = [getd.remote(b) for b in range(1,81)]

results = ray.get(settings)

# with ThreadPoolExecutor(max_workers=10) as pool:
#     for z in range(1, 81):
#         pool.submit(getd, z)

time_end = time.time()  # 记录结束时间
time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
print(time_sum)






