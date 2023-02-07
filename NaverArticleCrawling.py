from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re #정규표현식



# naverNews_url = "https://news.naver.com/main/list.naver?mode=LS2D&sid2=258&sid1=101&mid=shm&date=20230206&page=1" #1 ~ 51
# chrome_options = webdriver.ChromeOptions()
#
# wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# wd.get(naverNews_url)
# # time.sleep(1)
# html = wd.page_source
# soup = BeautifulSoup(html,'html.parser')
# # articles = soup.select('li ')
# articles = soup.select('li > dl')
# print(articles)



def getArticleScript(article_script_url)->str: #기사 본문을 리턴하는 메서드
    wd.get(article_script_url)
    time.sleep(1)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tmp = soup.select("div#dic_area")
    # print('tmp :', "type :",type(tmp),tmp)
    tag = re.compile('<.*?>') #<>태그를 모두 없앤다.
    script = ""
    for i in tmp:
        i = str(i)
        txt = re.sub(tag, '', i).strip()
        new_txt = txt.replace("\n", "")
        script = new_txt
    return script
        # print(new_txt)
        # script += txt.strip() + " "
        # print("본문 :",len(txt),type(txt),txt,"끝끝끝")



def getArticleDate(article_script_url):#기사 작성 날짜 반환
    wd.get(article_script_url)
    html = wd.page_source
    soup = BeautifulSoup(html, 'html.parser')
    date_tag = soup.select_one(
        "div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
    date_tag = str(date_tag)
    html_tag = re.compile('<.*?>')
    script_date = re.sub(html_tag, '', date_tag)
    return script_date



def getTitleMethod(article):#기사제목 반환, 가끔씩 이름이 두 개 들어갈때가 있음.
    ansStr = ""
    tag = re.compile('<.*?>')
    for i in article:
        i = str(i)
        txt = re.sub(tag, '', i).strip()
        if txt == "":
            continue
        ansStr = txt
    return ansStr


#################################################################################################################################################




arr = []
# for page in range(1,52):
for page in range(1,6):

    naverNews_url = "https://news.naver.com/main/list.naver?mode=LS2D&sid2=258&sid1=101&mid=shm&date=20230206&page={0}".format(page)
    print(naverNews_url)
    chrome_options = webdriver.ChromeOptions()
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wd.get(naverNews_url)
    html = wd.page_source
    soup = BeautifulSoup(html,'html.parser')
    articles = soup.select('li > dl')

    for index,article in enumerate(articles):
        raw_html = article.find_all('a')
        title = getTitleMethod(raw_html)

        #완료
        # print("제목 : ",title)
        article_script_url = article.find('a')['href']
        article_script = getArticleScript(article_script_url)
        # print('본론 :',article_script)
        # print("!!링크!! : ",article.find('a')['href'])
        script_date = getArticleDate(article_script_url)
        # print("언론사 : ",article.find_all(attrs={'class': re.compile('^writing')})[0].string )
        # print("작성 날짜 :",script_date)

        # one_Article = {}
        one_Article = dict()
        one_Article["title"] = title
        one_Article["press"] = article.find_all(attrs={'class': re.compile('^writing')})[0].string
        one_Article["date"] = script_date
        one_Article["article"] = article_script
        one_Article["article_link"] = article.find('a')['href']
        print(one_Article)
        arr.append(one_Article)
    print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★페이지 끝입니다.★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")





print("★★★★★★★★★★★★★★★★★크롤링 끝입니다.★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")
# for i in arr:
#     print(i)
import pymongo
conn = pymongo.MongoClient()
db = conn.bitDB







































