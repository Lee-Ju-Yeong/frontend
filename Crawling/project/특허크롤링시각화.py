import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
from matplotlib import font_manager, rc



# 엑셀 파일 읽기
file_path = 'C:\Toz\Crawling\project\머신러닝_특허_1000개_20240718_131704.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')


# 제목 줄이기 함수
def shorten_title(title, max_length=30):
    if len(title) > max_length:
        return title[:max_length//2] + "..." + title[-max_length//2:]
    return title

# 제목을 여러 줄로 나누기 함수
def wrap_title(title, max_length=20):
    words = title.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return "\n".join(lines)


# 날짜 컬럼이 있는 경우, 연도만 추출하여 새로운 컬럼 생성
df['Application Date'] = pd.to_datetime(df['Application Date'], format='%Y.%m.%d', errors='coerce')
df['Year'] = df['Application Date'].dt.year

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 윈도우의 경우 맑은고딕 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 형태소 분석기 초기화
okt = Okt()
# 불용어 목록

stopwords = set(['이', '그', '저', '것', '수', '있다', '등', '의', '가', '을', '를', '은', '는', '에', '과', '하고', '이다','머신','러닝','방법','기반','장치','이용','시스템','모델','활용'])

# 텍스트 데이터 전처리 및 명사 추출 함수
def preprocess_text(text):
    # 형태소 분석
    tokens = okt.nouns(text)
    # 한 글자 단어 및 불용어 제거
    tokens = [token for token in tokens if len(token) > 1 and token not in stopwords]
    return tokens

# 시기별 워드클라우드 생성 함수
def generate_wordcloud(dataframe, start_year=None, end_year=None):
    words = []
    if start_year and end_year:
        data = dataframe[(dataframe['Year'] >= start_year) & (dataframe['Year'] <= end_year)]
    else:
        data = dataframe

    for text in data['Title'].dropna():
        words.extend(preprocess_text(text))
    
    # 단어 빈도수 계산
    word_count = Counter(words)
    
    # 워드클라우드 생성
    wc = WordCloud(font_path=font_path,  # 한글 폰트 지정
                   background_color='white',
                   width=800,
                   height=600)
    wc.generate_from_frequencies(word_count)
    
    # 워드클라우드 시각화
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    if start_year and end_year:
        plt.title(f'{start_year}년부터 {end_year}년까지의 특허 제목 워드클라우드')
    else:
        plt.title('전체 특허 제목 워드클라우드')
    plt.show()



# 피인용 횟수 상위 10개 특허 시각화 함수
def visualize_top_cited(dataframe):
    top_cited = dataframe.sort_values(by='Citations', ascending=False).head(10)
    top_cited['Wrapped Title'] = top_cited['Title'].apply(lambda x: wrap_title(x, max_length=20))
    
    plt.figure(figsize=(12, 6))
    plt.barh(top_cited['Wrapped Title'], top_cited['Citations'], color='skyblue')
    plt.xlabel('Citations')
    plt.ylabel('Patent Title')
    plt.title('Top 10 Most Cited Patents')
    plt.gca().invert_yaxis()
    plt.show()


# 예시: 2019년부터 2021년까지의 워드클라우드 생성
generate_wordcloud(df, start_year=2019, end_year=2021)


# 피인용 횟수 상위 10개 특허 시각화
visualize_top_cited(df)

