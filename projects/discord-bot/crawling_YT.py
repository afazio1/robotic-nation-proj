from selenium import webdriver
from bs4 import BeautifulSoup
import time

#pip install lxml
#pip install beautifulsoup4
#pip install selenium
#exe파일 경로는 상대경로가 아닌 절대경로로 설정해야함.
#영상에 대한 댓글을 크롤링하는 함수
def Crawling_YT_Comment(comm):
    driver = webdriver.Chrome('Your absolute path of Chromedriver.exe')
    url = comm
    driver.get(url)

    driver.execute_script('return document.documentElement.scrollHeight')
    #화면상 스크롤 위치 이동 : scrollTo(x,Y) ,scrollTo(x,Y+number)
    #화면 최하단으로 스크롤 이동 : scrollTo(0, document.body.scrollHeight)
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    #Wait to load page
    time.sleep(3)

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
        str_tmp = str_tmp.strip()
        if len(str_tmp)>100:
            str_tmp = str_tmp[:100]
        youtube_Ids.append(str_tmp)

        str_tmp = str(yt_comment[i].text)
        str_tmp = str_tmp.replace('\n', '')
        str_tmp = str_tmp.replace('\t', '')
        str_tmp = str_tmp.replace('                ', '')
        str_tmp = str_tmp.strip()
        if len(str_tmp)>100:
            str_tmp = str_tmp[:100] + "...too many words"
        youtube_comments.append(str_tmp)

        str_tmp = str(yt_like[i].text)
        str_tmp = str_tmp.replace('\n', '')
        str_tmp = str_tmp.replace('\t', '')
        str_tmp = str_tmp.strip()
        if len(str_tmp)>100:
            str_tmp = str_tmp[:100]
        youtube_likes.append(str_tmp)

    return youtube_Ids, youtube_comments, youtube_likes

#유튜브 검색기능을 사용하여 검색된 영상들에 대한 제목과 url을 가져오는 함수
def Crawling_YT_Title(comm):
    driver = webdriver.Chrome('Your absolute path of Chromedriver.exe')
    url = "https://www.youtube.com/results?search_query={}".format(comm)
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

    if len(youtube_title)>5:
        return youtube_title[:5], youtube_href[:5]
    else:
        return youtube_title, youtube_href