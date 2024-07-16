from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd

#Block chrome closes immediately after being launched
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
#Create chrome webdriver object
driver = webdriver.Chrome(options=options)

# 원하는 날짜
input_date= input("검색할 날짜(yyyy-mm-dd)-->>")

# driver.maximize_window()
# time.sleep(1)

# #첫번째 아트클의 제목 
# soup.select_one(".articleSubject").text.strip('\n')

# #링크는 a태그 안에 속성을 가져와야해.
# soup.select_one(".articleSubject>a")

page=1 
article_list=[]

while True:
    time.sleep(3)
    url =f'https://finance.naver.com/news/mainnews.naver?date= {input_date}&page={page}'
    driver.get(url)
    # 페이지 소스를 다시 파싱하여 soup 객체 업데이트
    html = driver.page_source   
    soup = BeautifulSoup(html, 'html.parser')

    # 기사 목록 선택
    articles = soup. select(".block1")
    for article in articles:
        title = article.select_one(".articleSubject").text.strip('\n')
        url = article.select_one(".articleSubject>a").attrs["href"]
        summary = article.select_one(".articleSummary").text.strip('\n')
        # summary에서 press와 wdate 부분을 제외한 텍스트 추출
        # press와 wdate를 기준으로 분할하여 summary를 추출
        
        press=article.select_one(".press").text
        date=article.select_one(".wdate").text
        ## by.AI
        # full_text = article.get_text(separator=' ', strip=True)
        # summary = full_text.replace(press, '').replace(date, '').replace('|', '').strip()
    
        # by.강사님
        summary= article.select_one(".articleSummary").contents[0].strip()
        article_list.append([title,url,summary,press,date])
        # print(title)

    print(page)
    page+=1
    # 다음 페이지가 있는지 확인 (맨뒤 아이콘을 찾아 마지막 페이지 확인)
    last_page_link = soup.select_one(".pgRR>a")
    if last_page_link:
        last_page_link_num = int(last_page_link.attrs["href"].split("page=")[-1])
        if page > last_page_link_num:
            break
    else:
        break
df= pd.DataFrame(article_list,
                 columns=['title','url','summary','press','date'])


file_name  = f'네이버 증권뉴스_{input_date.replace('-','')}'#파일명 생성

# CSV 파일로 저장
df.to_csv(file_name+'.csv', index=False, encoding='utf-8-sig')
print("CSV 파일로 저장되었습니다.")

driver.quit()
