from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

# WebDriver 초기화 (PATH에 추가했기 때문에 executable_path를 사용하지 않음)
browser = webdriver.Chrome()

# 접속 url
url = "https://youtube.com/"

# 검색 키워드
keyword = "나혼자 여행"

# 스크롤을 어디까지 내리는지 기준 
# finish_line = 40000 기준: 162 개
finish_line = 10000

browser.maximize_window()
browser.get(url)
time.sleep(2)
search = browser.find_element(By.NAME, "search_query")
time.sleep(2)
search.send_keys(keyword)
search.send_keys(Keys.ENTER)

# 검색 후 url 작업창 변경 (파싱)
present_url = browser.current_url
browser.get(present_url)
last_page_height = browser.execute_script("return document.documentElement.scrollHeight")

# 스크롤 100번 수행
scroll_count = 0
while scroll_count < 100:
    # 우선 스크롤 내리기
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2.0)       # 작업 중간에 1이상으로 간격을 줘야 데이터 취득가능(스크롤을 내릴 때의 데이터 로딩 시간 때문)
    # 현재 위치 담기
    new_page_height = browser.execute_script("return document.documentElement.scrollHeight")
    
    # 스크롤 횟수 증가
    scroll_count += 1

html_source = browser.page_source
soup = BeautifulSoup(html_source, 'html.parser')

# finish line까지 모든 검색 결과 정보 가져오기
# 모든 컨텐츠 관련 부분을 떼어내기
# find_all: 해당 정보의 모든 부분 가져오기
elem = soup.find_all("ytd-video-renderer", class_="style-scope ytd-item-section-renderer")

# 필요한 정보 가져오기
df = []
for t in elem[:100]:  # 처음 100개의 동영상 정보만 가져오도록 수정
    title = t.find("yt-formatted-string", class_="style-scope ytd-video-renderer").get_text()
    name = t.find("a", class_="yt-simple-endpoint style-scope yt-formatted-string").get_text()
    content_url = t.find("a", class_="yt-simple-endpoint style-scope ytd-video-renderer")["href"]
    df.append([name, title , 'https://www.youtube.com/'+content_url])

## 자료 저장
# 데이터 프레임 만들기
new = pd.DataFrame(columns=['name', 'title' , 'url_link'])

# 자료 집어넣기
for i in range(len(df)):
    new.loc[i] = df[i]

# 데이터를 저장할 디렉토리 생성
df_dir = "./data/"
if not os.path.exists(df_dir):
    os.makedirs(df_dir)

# 저장하기
new.to_csv(os.path.join(df_dir, "Youtube_search_df.csv"), index=True, encoding='utf8')  # 인덱스 포함하여 저장

## 컬럼 정보 저장
# 컬럼 설명 테이블
col_names = ['name', 'title' ,'url_link']
col_exp = ['컨텐츠 올린 채널명', '컨텐츠 제목', '연결 링크']

new_exp = pd.DataFrame({'col_names':col_names,
                        'col_explanation':col_exp})

# 저장하기
new_exp.to_csv(os.path.join(df_dir, "Youtube_col_exp.csv"), index=False, encoding='utf8')

# 브라우저 닫기
browser.close()
