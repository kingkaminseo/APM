import urllib.request as req
from bs4 import BeautifulSoup
import pandas as pd
import os

# 웹 페이지에서 데이터 스크래핑
url = "https://www.melon.com/chart/index.htm"
headers = {"User-Agent": "Mozilla/5.0"}
code = req.urlopen(req.Request(url, headers=headers))
soup = BeautifulSoup(code, "lxml")

titles = []
artists = []
albums = []
image_urls = []

title_elements = soup.select("div.ellipsis.rank01 a")
artist_elements = soup.select("div.ellipsis.rank02 span.checkEllipsis")
album_elements = soup.select("div.ellipsis.rank03 a")
image_elements = soup.select("a.image_typeAll img")

for title_element, artist_element, album_element, image_element in zip(title_elements, artist_elements, album_elements, image_elements):
    titles.append(title_element.text)
    artists.append(artist_element.text)
    albums.append(album_element.text)
    image_urls.append(image_element["src"])

# 데이터를 DataFrame으로 만들기
data = {
    "Title": titles,
    "Artist": artists,
    "Album": albums,
    "ImageURL": image_urls
}
df = pd.DataFrame(data)

# CSV 파일로 저장
csv_filename = "melon_chart.csv"
df.to_csv(csv_filename, index=False)

print(f"Data has been saved to {csv_filename}.")
