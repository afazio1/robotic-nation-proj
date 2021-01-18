from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome('./chromedriver.exe')
url = "https://www.youtube.com/results?search_query={}".format("아이유")
driver.get(url)

html_src = driver.page_source
driver.close()

soup = BeautifulSoup(html_src, 'lxml')

yt_info = soup.select("a#video-title")

youtube_title = []
youtube_href = []

for i in range(len(yt_info)):
    youtube_title.append(yt_info[i].text.strip())
    youtube_href.append('{}{}'.format('https://www.youtube.com',yt_info[i].get('href')))

for i in range(len(youtube_title)):
    print(youtube_title[i], youtube_href[i])