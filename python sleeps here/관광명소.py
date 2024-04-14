import os
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('incognito')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")

browser = webdriver.Chrome(options=options)

browser.get("https://korean.visitkorea.or.kr/list/all_list.do?choiceTag=&choiceTagId=")

def finds(css_selector):
    return browser.find_elements(By.CSS_SELECTOR, css_selector)

def find(css_selector):
    return browser.find_element(By.CSS_SELECTOR, css_selector)

def finds_xpath(xpath):
    return browser.find_elements(By.XPATH, xpath)

regions = {
    '1': '서울',
    '2': '인천',
    '3': '대전',
    '4': '대구',
    '6': '부산',
    '31': '경기도',
    '32': '강원도',
    '33': '충청도',
    '35': '경상도',
    '37': '전라도',
}

# 각 조합된 지역별 빈 데이터프레임 생성
combined_regions = {
    '전라도': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '경상도': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '충청도': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '서울': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '인천': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '대전': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '대구': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '부산': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '경기도': pd.DataFrame(columns=['title', 'place', 'img_scr']),
    '강원도': pd.DataFrame(columns=['title', 'place', 'img_scr'])
}

# 각 지역에 대해 반복
for region_id in regions:
    if region_id in ['34', '36', '38']:  # 빈 지역 건너뛰기
        continue

    wait = WebDriverWait(browser, 10)  # 클릭 가능한 요소를 찾을 때까지 최대 10초 대기
    click_tag = None

    for _ in range(5):  # 최대 5번까지 재시도
        try:
            click_tag = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"li[id='{region_id}'] > button")))
            break  # 요소를 찾으면 루프를 종료
        except TimeoutException:
            print("요소를 찾을 수 없습니다. 다시 시도 중...")
            time.sleep(5)  # 5초 대기 후 재시도

    if click_tag is None:
        print("요소를 찾을 수 없습니다.")
        # 필요한 경우 예외 처리나 오류 메시지를 추가할 수 있습니다.
    else:
        click_tag.click()

    time.sleep(3)
    time.sleep(5)

    img_scr = []
    title = []
    place_info = []

    # 페이지별로 반복
    for i in range(1, 31):
        search_imgs = finds("div[class='photo'] > a > img")
        for img in search_imgs:
            img_scr.append(img.get_attribute('src'))

        search_text = finds("div[class='tit'] > a")
        for text in search_text:
            title.append(text.text)

        search_place = finds_xpath("//*/div/div/ul/li/div/p[1]")
        for place in search_place:
            place_info.append(place.text)

        click_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div[class='page_box'] > a[id='{i}']")))
        click_btn.click()

        time.sleep(5)

    data = {"title": title, "place": place_info, "img_scr": img_scr}
    df = pd.DataFrame(data)

    # 데이터 전처리
    df = df.drop_duplicates()
    df['title'] = df['title'].str.replace(r'\[.*?\]', '').str.strip()
    df['title'] = df['title'].str.replace('(Game Show & Trade, All-Round)', '')
    df['title'] = df['title'].str.replace(r'\(\)', '').str.strip()

    dr = df[df['img_scr'].str.contains('undefined')].index
    df.drop(dr, inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.columns = df.columns.str.replace(' ', '')

    df_2 = df.copy()
    df_2['title'] = df_2['title'].str.replace(',', '')

    region_name = regions[region_id]
    combined_regions[region_name] = pd.concat([combined_regions[region_name], df.head(30)], ignore_index=True)

# 폴더 생성
folder_name = "관광지 크롤링"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# CSV 파일로 저장
for region_name, df in combined_regions.items():
    csv_filename = os.path.join(folder_name, f"{region_name}.csv")
    df.to_csv(csv_filename, index=False)

browser.close()
