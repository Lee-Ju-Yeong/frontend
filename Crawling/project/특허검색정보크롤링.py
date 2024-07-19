from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import math
import random
from datetime import datetime


#Block chrome closes immediately after being launched
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
#Create chrome webdriver object
driver = webdriver.Chrome(options=options)

# 웹페이지 접근
url = 'http://kpat.kipris.or.kr/kpat/searchLogina.do?next=MainSearch'
driver.get(url)
time.sleep(1)

# HTML 문자열을 파싱하여 BeautifulSoup 객체 생성
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# 요소 지정하기(여기선 검색창)
search = driver.find_element(By.CSS_SELECTOR, "#queryText") 
# 요소 클릭하기
search.click()
# 요소에 단어 입력하기
input_word=input("크롤링할 단어를 입력하세요 : ")

# 순차적으로 엔터키 입력하기->검색 작동
search.send_keys(input_word, Keys.ENTER)

time.sleep(3)  # 페이지가 로드될 시간을 줌

# 분석에 필요한 특허 개수 입력 받기
num_patents_required = int(input("분석에 필요한 특허 개수를 입력하세요 : "))

# 페이지당 특허 수(이건 기본페이지에서 정해져있음)
patents_per_page = 30

# 필요한 페이지 수 계산
num_pages_required = math.ceil(num_patents_required / patents_per_page)

특허_list = []
#데이터 크롤링 함수
def extract_data():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    특허s = soup.select('.search_section>article')
    
    for 특허 in 특허s:
        try:
            # 상태 (등록인지 취소인지)
            status_element = 특허.select_one('h1.stitle a')
            status = status_element.text.strip() if status_element else 'N/A'
            
            # 제목
            title_element = 특허.select_one('.search_section_title > h1 > a:nth-child(2)')
            title_full  = title_element.text.strip() if title_element else 'N/A'
            # 제목과 영어제목 분리
            if '(' in title_full and ')' in title_full:
                title, title_en = title_full.split('(', 1)
                title_en = title_en.rstrip(')')
            else:
                title, title_en = title_full, 'N/A'

            # IPC 코드들
            IPC_elements = 특허.select('.search_info_list .mainlist_topinfo li:nth-child(1) span.point01')
            IPC_codes = [ipc.text.strip() for ipc in IPC_elements]
            IPC = ', '.join(IPC_codes)  # 여러 개의 IPC 코드를 콤마로 구분하여 문자열로 변환
            
            # 출원번호(일자)
            numdate_element = 특허.select_one('.search_info_list .mainlist_topinfo li:nth-child(3) a')
            
            if numdate_element:
                numdate_text = numdate_element.text.strip()
                num, date = numdate_text.split(' (')
                date = date.rstrip(')')
            else:
                num, date = 'N/A', 'N/A'
            
            # 출원인 
            applicant_element = 특허.select_one('#mainsearch_info_list > div.mainlist_topinfo > li:nth-child(4) > a > font')
            applicant = applicant_element.text.strip() if applicant_element else 'N/A'
            
            # 최종권리자 
            holder_element = 특허.select_one('#mainsearch_info_list > div.mainlist_topinfo > li.left_width.letter1 > span.point01 > a > font')
            holder = holder_element.text.strip() if holder_element else 'N/A'
            
            # citations 인용횟수
            try:
                citations_element = 특허.select_one('#mainsearch_info_list > div.mainlist_topinfo > li:nth-child(6) > span.point01 > a')
                # print(citations_element)
                citations = citations_element.text.strip() if citations_element else 'N/A'
            except Exception as e:
                citations = 'N/A'
            
            # 요약
            abstract_element = 특허.select_one('.search_txt')
            abstract = abstract_element.text.strip() if abstract_element else 'N/A'

            특허_list.append([status, title, title_en, IPC, num, date, applicant, holder, citations, abstract])
        except Exception as e:
            print(f"Error extracting data: {e}")

# 페이지를 돌면서 (필요한 데이터 숫자에 따라 페이지수가 달라짐)
for page in range(num_pages_required):
    extract_data()
    if page < num_pages_required - 1:  # 마지막 페이지에서는 '다음' 버튼을 클릭하지 않음
        try:
            current_page = (page % 10) + 1
            #10번 페이지, 20번페이지, 30번페이지, 즉 10배수 페이지에서는 다음페이지버튼을 누름
            if current_page == 10:
                next_button = driver.find_element(By.CSS_SELECTOR, '.board_pager03 a.next')
                next_button.click()
                
            else:
                next_page_number = current_page + 1
                next_page_button = driver.find_element(By.XPATH, f"//a[text()='{next_page_number}']")
                next_page_button.click()
            # 5초에서 11초 사이의 랜덤 시간 대기
            time.sleep(random.uniform(5, 11))
        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            break
# 필요한 개수만큼 데이터 슬라이싱(잘라냄, 예를들면 308개가 필요하면 11페이지를 가져올텐데 330개의 데이터중에 308개까지 자름)
특허_list = 특허_list[:num_patents_required]


# 현재 시간 설정(파일이름에 반영하기위해)
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
# 파일명 생성(검색어,검색량,현재시간으로 구성)
file_name = f"{input_word}_특허_{num_patents_required}개_{current_time}.xlsx"
# 데이터프레임으로 변환 및 CSV 파일로 저장
df = pd.DataFrame(특허_list, columns=['Status', 'Title', 'Title_EN', 'IPC', 'Application Number', 'Application Date', 'Applicant', 'Holder', 'Citations', 'Abstract'])
df.to_excel(file_name, index=False, engine='openpyxl')

# 브라우저 종료
driver.quit()

print("데이터 수집 완료")



