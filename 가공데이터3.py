import pandas as pd
import numpy as np

df = pd.read_csv('가공데이터3.csv', sep=',') 
df.columns = ['name', 'food', 'number', 'add']
df.columns 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

chromedriver = 'C:/Users/yoonsung/Desktop/셀레늄/chromedriver.exe' 
driver = webdriver.Chrome(chromedriver) 

df['kakao_keyword'] = df['add'] + "%20" + df['name']
df['kakao_map_url'] = ''


for i, keyword in enumerate(df['kakao_keyword'].tolist()):
    print("이번에 찾을 키워드 :", i, f"/ {df.shape[0]} 행", keyword)
    try:
        kakao_map_search_url = f"https://map.kakao.com/?q={keyword}"
        driver.get(kakao_map_search_url)
        time.sleep(3.5)
        df.iloc[i,-1] = driver.find_element_by_css_selector("#info\.search\.place\.list > li:nth-child(1) > div.info_item > div.contact.clickArea > a.moreview").get_attribute('href')
    except Exception as e1:
        if "li:nth-child(1)" in str(e1):
            try:
                df.iloc[i,-1] = driver.find_element_by_css_selector("#info\.search\.place\.list > li > div.info_item > div.contact.clickArea > a.moreview").get_attribute('href')
                time.sleep(1)
            except Exception as e2:
                print(e2)
                df.iloc[i,-1] = np.nan
                time.sleep(1)
        else:
            pass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

chromedriver = 'C:/Users/yoonsung/Desktop/셀레늄/chromedriver' 
driver = webdriver.Chrome(chromedriver) 

kakao_map_name_list = []
blog_review_list = []
blog_review_qty_list = []
kakao_map_star_review_stars_list = []
kakao_map_star_review_qty_list = []

for i, url in enumerate(df['kakao_map_url']):
    driver.get(url)
    time.sleep(1)
    review_text = ""
    
    try:
        
        kakao_map_name = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > h2").text
        blog_review_qty = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(5) > span").text
        star_review_stars = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b.inactive").text
        star_review_qty = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_g").text
    except Exception as e1:
        if "inactive" in str(e1):
            star_review_stars = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_b").text
            star_review_qty = driver.find_element_by_css_selector("#mArticle > div.cont_essential > div:nth-child(1) > div.place_details > div > div > a:nth-child(3) > span.color_g").text
        else:
            print(f"{num}행 데이터의 평점 갯수 크롤링에 다른 문제가 생겼다")
            
    num = 0
    try:
        while num < 3:
            try:
                num += 1
                review_text = review_text + driver.find_element_by_css_selector(f"div.wrap_list > ul > li:nth-child({num}) > a > div.review_story > p").text
                
                if num == 3:
                    blog_review_list.append(review_text)  # 3개나 찾았으면 그만 찾고 나감
                    kakao_map_name_list.append(kakao_map_name)
                    blog_review_qty_list.append(blog_review_qty)
                    kakao_map_star_review_stars_list.append(star_review_stars)
                    kakao_map_star_review_qty_list.append(star_review_qty)
                    
                    break
            except Exception as e1:
                if "li:nth-child(1)" in str(e1):  # child(1)이 없던데요? -> 리뷰가 하나도 없는 것
                    print(f"{i}행은 리뷰가 없네")
                    review_text = "empty"
                    blog_review_list.append(review_text)
                    kakao_map_name_list.append(kakao_map_name)
                    blog_review_qty_list.append(blog_review_qty)
                    kakao_map_star_review_stars_list.append(star_review_stars)
                    kakao_map_star_review_qty_list.append(star_review_qty)
                    break
                else:
                    print(f"{i}행 문제가 발생 - 리뷰가 {num - 1}개뿐이다")
                    blog_review_list.append(review_text)  # 일단 리뷰가 하나도 없는 건 아니니 붙이고 탈출 / 리뷰 딸랑 하나 있으면 발생할 수 있음                    
                    kakao_map_name_list.append(kakao_map_name)
                    blog_review_qty_list.append(blog_review_qty)
                    kakao_map_star_review_stars_list.append(star_review_stars)
                    kakao_map_star_review_qty_list.append(star_review_qty)
                    break
                
    except Exception as e2:
        print(e2)
        print(f"{i}행 문제가 발생 - code 2")
driver.quit()


df['kakao_store_name'] = kakao_map_name_list  # 카카오 상세페이지에서 크롤링한 상호명
df['kakao_star_point'] = kakao_map_star_review_stars_list  # 카카오 상세페이지에서 평가한 별점 평점
df['kakao_star_point_qty'] = kakao_map_star_review_qty_list  # 카카오 상세페이지에서 별점 평가를 한 횟수
df['kakao_blog_review_txt'] = blog_review_list  # 카카오 상세페이지에 나온 블로그 리뷰 텍스트들
df['kakao_blog_review_qty'] = blog_review_qty_list  # 카카오 상세페이지에 나온 블로그 리뷰의 총 개수

df['cate_mix'] = df['food']
df['cate_mix'] = df['cate_mix'].str.replace("/", " ")

from sklearn.feature_extraction.text import CountVectorizer  # 피체 벡터화
from sklearn.metrics.pairwise import cosine_similarity  # 코사인 유사도


count_vect_category = CountVectorizer(min_df=0, ngram_range=(1,2))
place_category = count_vect_category.fit_transform(df['cate_mix']) 
place_simi_cate = cosine_similarity(place_category, place_category) 
place_simi_cate_sorted_ind = place_simi_cate.argsort()[:, ::-1]
count_vect_review = CountVectorizer(min_df=2, ngram_range=(1,2))
place_review = count_vect_review.fit_transform(df['kakao_blog_review_txt']) 

place_simi_review = cosine_similarity(place_review, place_review)
place_simi_review_sorted_ind = place_simi_review.argsort()[:, ::-1]
place_simi_co = (
                 + place_simi_cate * 0.3 # 카테고리 유사도
                 + place_simi_review * 1 # 리뷰 텍스트 유사도
                )



place_simi_co_sorted_ind = place_simi_co.argsort()[:, ::-1] 


def find_simi_place(df, sorted_ind, cate):
    
    place_title = df[df['food'] == cate]
    place_index = place_title.index.values
    similar_indexes = sorted_ind[place_index, :(1)]
    similar_indexes = similar_indexes.reshape(-1)
    return df.iloc[similar_indexes]
