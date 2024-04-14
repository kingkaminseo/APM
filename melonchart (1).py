from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

url = "https://www.melon.com/chart/index.htm"

r = requests.get(url, headers=headers)

print(r.raise_for_status)

html = r.text

soup = BeautifulSoup(html, "html.parser")

lst50 = soup.select(".lst50")

lst100 = soup.select(".lst100")

lst = lst50 + lst100

print(len(lst))

for e, i in enumerate(lst, 1):
    print(f"<<{e}위>>")
    title = i.select_one(".ellipsis.rank01 a")
    print(title.text)

    singers = i.select(".ellipsis.rank02 > a")
    for singer in singers:
        print(singer.text)

    album = i.select_one(".ellipsis.rank03 > a")
    print(album.text)

    print()