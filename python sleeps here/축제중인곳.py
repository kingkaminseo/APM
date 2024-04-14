import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('incognito')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")

browser = webdriver.Chrome(options=options)

browser.get("https://korean.visitkorea.or.kr/list/all_list.do?choiceTag=&choiceTagId=")

wait = WebDriverWait(browser, 10)

# Find the button for the desired region (전체 in this case) using XPath
region_xpath = '//*[@id="b8b89ce0-35d8-4127-a429-0aecd20891e9"]/button/span'
click_tag = wait.until(EC.element_to_be_clickable((By.XPATH, region_xpath)))
click_tag.click()

# Wait for the page to load
time.sleep(5)

img_scr = []
title = []
place_info = []

# Loop through elements on the current page (up to 5)
for i in range(1, 6):
    search_imgs = browser.find_elements(By.CSS_SELECTOR, "div[class='photo'] > a > img")
    img_scr.append(search_imgs[i - 1].get_attribute('src'))

    search_text = browser.find_elements(By.CSS_SELECTOR, "div[class='tit'] > a")
    title.append(search_text[i - 1].text)

    search_place = browser.find_elements(By.XPATH, "//*/div/div/ul/li/div/p[1]")
    place_info.append(search_place[i - 1].text)

# Create a DataFrame
data = {"title": title, "place": place_info, "img_scr": img_scr}
df = pd.DataFrame(data)

# Data preprocessing
df = df.drop_duplicates()
df['title'] = df['title'].str.replace(r'\[.*?\]', '').str.strip()
df['title'] = df['title'].str.replace('(Game Show & Trade, All-Round)', '')
df['title'] = df['title'].str.replace(r'\(\)', '').str.strip()

dr = df[df['img_scr'].str.contains('undefined')].index
df.drop(dr, inplace=True)
df.reset_index(drop=True, inplace=True)

df.columns = df.columns.str.replace(' ', '')

# 폴더 생성
folder_name = "지금 축제 중인 곳"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Save to '현재 축제 top5.csv' file within the folder
csv_filename = os.path.join(folder_name, "현재 축제 top5.csv")
df.to_csv(csv_filename, index=False)

browser.close()