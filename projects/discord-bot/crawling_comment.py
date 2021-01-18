from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome('./chromedriver.exe')
url = 'https://www.youtube.com/watch?v=EXEU6Skp7Qs'
driver.get(url)

last_page = driver.execute_script('return document.documentElement.scrollHeight')

while True:
    #화면상 스크롤 위치 이동 : scrollTo(x,Y) ,scrollTo(x,Y+number)
    #화면 최하단으로 스크롤 이동 : scrollTo(0, document.body.scrollHeight)
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    #Wait to load page
    time.sleep(1)
    #scroll height is last height? 
    new_page = driver.execute_script("return document.documentElement.scrollHeight")

    if new_page == last_page:
        break
    last_page = new_page

html_src = driver.page_source
driver.close()

soup = BeautifulSoup(html_src, 'lxml')

yt_id = soup.select("div#header-author > a > span")
yt_comment = soup.select("yt-formatted-string#content-text")
yt_like = soup.select("div#toolbar>span")

youtube_Ids = []
youtube_comments = []
youtube_likes = []

for i in range(len(yt_id)):
    str_tmp = str(yt_id[i].text)
    str_tmp = str_tmp.replace('\n', '')
    str_tmp = str_tmp.replace('\t', '')
    str_tmp = str_tmp.replace('                ', '')
    youtube_Ids.append(str_tmp)

    str_tmp = str(yt_comment[i].text)
    str_tmp = str_tmp.replace('\n', '')
    str_tmp = str_tmp.replace('\t', '')
    str_tmp = str_tmp.replace('                ', '')
    youtube_comments.append(str_tmp)

    str_tmp = str(yt_like[i].text)
    youtube_likes.append(int(str_tmp))

for i in range(len(youtube_Ids)):
    print(youtube_Ids[i], youtube_comments[i], youtube_likes[i])