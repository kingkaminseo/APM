import os
import csv
import requests
from bs4 import BeautifulSoup

def scrape_hotel_data(uri):
    response = requests.get(uri)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 박스 값
    bigbox = soup.find(id="product_filter_form")
    middlebox = bigbox.find(id="content")
    hotellistbox = middlebox.find(id="poduct_list_area")

    # 이미지, 이름, 이름 리스트 추출
    namelist = []
    imglist = []

    imgclass = hotellistbox.find_all(class_="lazy")

    for i in range(len(imgclass)):
        namelist.append(imgclass[i]['alt'])

    for i in range(len(imgclass)):
        imglist.append(imgclass[i]['src'])

    # 링크, 위치, 가격 데이터 추출
    hotellist = []
    locationlist = []
    pricelist = []

    alist = hotellistbox.find_all('a')
    Llist = hotellistbox.select('.stage')
    pdata = hotellistbox.select(".price")

    for link in alist:
        hotellist.append(link.get('href'))

    for loc in Llist:
        try:
            localdata = loc.find(class_='name')
            localdata.div.extract()
            localdata.find(class_='score').extract()
            localdata.find('strong').extract()
            localdata.find(class_="txt_evt").extract()

            local = localdata.text.strip()
            locationlist.append(local)
        except Exception:
            pass

    for p in pdata:
        try:
            pdata = p.find(class_='map_html')
            pdata.find('em').extract()

            price = pdata.text
            pricelist.append(price)
        except Exception:
            pass

    datarow = ["name", "link", "location", "price", "image"]
    datalist = []

    for i in range(len(namelist)):
        datalist.append(namelist[i])
        datalist.append(hotellist[i])
        datalist.append(locationlist[i] if i < len(locationlist) else "")
        datalist.append(pricelist[i] if i < len(pricelist) else "")
        datalist.append(imglist[i])

    return datarow, datalist

def Callthedata():
    regions = [
        "서울", "경기도", "부산", "충청도", "전라도", 
        "경상도", "인천", "대구", "대전", "강원도"
    ]

    base_url = "https://www.goodchoice.kr/product/result?keyword={}"

    folder_name = "숙소 크롤링"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for region in regions:
        uri = base_url.format(region)
        datarow, datalist = scrape_hotel_data(uri)

        filename = f"{region}.csv"
        filepath = os.path.join(folder_name, filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(datarow)
            for data in zip(*[iter(datalist)] * len(datarow[:-1])):
                data = list(data)
                image = data.pop(-1)
                data.insert(-1, image)
                writer.writerow(data)

    return f"Data saved to {folder_name} folder for multiple regions"

result = Callthedata()
print(result)