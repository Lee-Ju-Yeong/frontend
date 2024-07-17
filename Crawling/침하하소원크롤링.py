from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import math

#Block chrome closes immediately after being launched
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
#Create chrome webdriver object
driver = webdriver.Chrome(options=options)

# 웹페이지 접근
url = 'https://chimhaha.net/check'
driver.get(url)
# driver.maximize_window() 
time.sleep(5)

wish_list = []

def extract_data():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    wishes = soup.select('.item')
    
    for wish in wishes:
        try:
            # 순번
            number = wish.select_one('.number').text
            print(number)
            # 닉네임
            nickName = wish.select_one('.nickName').text
            print(nickName)
            # 소원
            comment = wish.select_one('.comment').text
            print(comment)
            # 연속날짜
            continue_ = wish.select_one('.continue').text
            print(continue_)
            # 총 소원빈 횟수
            total = wish.select_one('.total').text
            print(total)
            wish_list.append([number, nickName, comment, continue_, total])
        except Exception as e:
            print(f"Error extracting data: {e}")

# 데이터 수집 및 이전날로 이동
for _ in range(17):  # 예시로 5일치 데이터를 수집
    extract_data()
    try:
        prev_button = driver.find_element(By.XPATH, '//section[@class="buttons"]/a[text()="이전날"]')
        prev_button.click()
        time.sleep(5)  # 페이지가 로드될 시간을 줌
    except Exception as e:
        print(f"Error navigating to previous day: {e}")
        break
# 데이터프레임으로 변환 및 CSV 파일로 저장
df = pd.DataFrame(wish_list, columns=['순번', '닉네임', '소원', '연속날짜', '총 소원빈 횟수'])
df.to_csv('scraped_data.csv', index=False)

# 브라우저 종료
driver.quit()

print("데이터 수집 완료")
