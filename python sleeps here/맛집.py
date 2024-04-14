import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import warnings
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import platform
import os 

# Chrome 실행 파일 경로 설정
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if platform.system() == 'Darwin':  # macOS인 경우
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

options = Options()
options.binary_location = chrome_path

# chromedriver.exe 파일 경로 설정
chromedriver_path = "/path/to/chromedriver"
if platform.system() == 'Darwin':  # macOS인 경우
    chromedriver_path = "/path/to/chromedriver"

service = Service(chromedriver_path)


# 크롤링할 사이트 URL 리스트
urls = [
    "https://www.mangoplate.com/top_lists/KJU7_J7",
    "https://www.mangoplate.com/top_lists/2963_gangwondo2022",
    "https://www.mangoplate.com/top_lists/2749_gyeongsangdo2021",
    "https://www.mangoplate.com/top_lists/3119_gyeonggido2023",
    "https://www.mangoplate.com/top_lists/KSWVV24",
    "https://www.mangoplate.com/top_lists/1259_daejeon",
    "https://www.mangoplate.com/top_lists/2965_busan2022",
    "https://www.mangoplate.com/top_lists/ABRDRL2",
    "https://www.mangoplate.com/top_lists/2751_jeollado2021",
    "https://www.mangoplate.com/top_lists/2964_jejudo2022",
    "https://www.mangoplate.com/top_lists/2752_chungcheongdo2021"
]

# options = Options()
# options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # Chrome 실행 파일 경로
# service = Service(r'C:\Path\to\chromedriver.exe')  # chromedriver.exe 파일 경로

classname = [
    "서울",
    "강원도",
    "경상도",
    "경기도",
    "대구",
    "대전",
    "부산",
    "인천",
    "전라도",
    "제주도",
    "충청도"
]

for i, url in enumerate(urls):
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(3)

    name = []
    point = []
    address = []
    imgurl = []

    for _ in range(1):  # 더보기 버튼을 2번 클릭
        some_tag = driver.find_element(By.CSS_SELECTOR, '#contents_list > div > button')
        action = ActionChains(driver)
        action.move_to_element(some_tag).perform()
        some_tag.click()
        time.sleep(2)
        html = driver.page_source
        mang = BeautifulSoup(html, 'html.parser')

        list_soup = mang.find_all('div', 'info')
        for item in list_soup:
            address.append(item.find('p', 'etc').text.strip())
            point.append(item.find('strong', 'point').text.strip())
            title = item.find('span', 'title').text.strip()
            name.append(title[3:])

        images = driver.find_elements(By.CSS_SELECTOR, ".center-croping.lazy")
        for image in images:
            src = image.get_attribute('data-original')
            imgurl.append(src)

    driver.quit()

    name = name[:19]
    point = point[:19]
    address = address[:19]
    imgurl = imgurl[:19]

    data = {
        "foods": name,
        'Point': point,
        'Address': address,
        "imgurl": imgurl
    }

    df = pd.DataFrame(data)

    folder_name = "맛집 찾기"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    filename = f'{folder_name}/맛집{classname[i]}.csv'
    df.to_csv(filename, header=None, index=False, sep=',', encoding='utf-8')