import time

import cv2
import numpy as np
# import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import 기대_수명_예측
import 당뇨병_진행도_예측_랜덤_포레스트
import 연도별_국가_평균_수명_시각화
import 머신_러닝으로_얼굴_인식_후_성별_나이_출력
import 국가_평균_수명_예측

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])


# 아래 경로로 요청이 들어올때 해당 함수를 실행
@app.route('/predict_future', methods=['POST'])
def predict_future():
    # 리액트로부터 받은 데이터 추출
    data = request.json
    year = data['Year']
    country = data['Country']

    print("리액트로부터 받은 나라 및 연도 데이터 : " + str(data))

    # 예측 모델에 데이터 전달
    prediction, correlations, x, y = 국가_평균_수명_예측.predict_future(country, year)

    # JSON 형태로 결과 반환
    return jsonify({
        'prediction': prediction,
        'correlations': correlations,
        'x': x,
        'y': y
    })


@app.route('/predict_life_expectancy', methods=['POST'])
def predict_life_expectancy():
    # 리액트로부터 받은 데이터 추출
    data = request.json
    year = data['Year']
    bmi = data['BMI']
    alcohol = data['Alcohol']
    country = data['Country']

    print("리액트로부터 받은 기대 수명 예측 데이터 : " + str(data))

    # 예측 모델에 데이터 전달
    prediction, feature_importances, correlation, correlation_x, correlation_y, bmiA, alcohol, alcohol_a = 기대_수명_예측.predict_life_expectancy(
        year,
        bmi,
        alcohol,
        country)

    # JSON 형태로 결과 반환
    return jsonify({
        'prediction': prediction,  # 기대 수명
        'feature_importances': feature_importances,  # 특성 중요도
        'correlation': correlation,  # 상관 계수
        'correlation_x': correlation_x,
        'correlation_y': correlation_y,
        'bmiA': bmiA,
        'alcohol': alcohol,
        'alcoholA': alcohol_a
    })


@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes():
    # 리액트로부터 받은 데이터 추출
    data = request.json
    age = data['Age']
    bmi = data['BMI']
    bp = data['Bp']
    gender = data['Gender']

    print("리액트로부터 받은 기대 수명 예측 데이터 : " + str(data))

    # 예측 모델에 데이터 전달
    prediction, feature_importances, correlation, correlation_x, correlation_y = 당뇨병_진행도_예측_랜덤_포레스트.diabetes_Random(
        age, bmi, bp, gender)

    # JSON 형태로 결과 반환
    return jsonify({
        'prediction': prediction,  # 기대 수명
        'feature_importances': feature_importances,  # 특성 중요도
        'correlation': correlation,  # 상관 계수
        'correlation_x': correlation_x,
        'correlation_y': correlation_y,
    })


@app.route('/visualize_country', methods=['POST'])
def visualize_country():
    # 리액트로부터 받은 데이터 추출
    data = request.json
    country = data['Country']
    print("리액트로부터 받은 기대 수명 예측 데이터 : " + str(data))

    # 예측 모델에 데이터 전달
    data = 연도별_국가_평균_수명_시각화.avarage_life(country)

    # JSON 형태로 결과 반환
    return jsonify(data)


@app.route('/predict_face', methods=['POST'])
def predict_face():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        in_memory_file = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(in_memory_file, cv2.IMREAD_COLOR)

        results = 머신_러닝으로_얼굴_인식_후_성별_나이_출력.machine_face(img)
        return jsonify({'results': results})

    return jsonify({'error': 'Unknown error occurred'}), 500


@app.route('/search-news', methods=['GET'])
def search_news():
    query = request.args.get('query')

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저를 띄우지 않는 옵션
    chrome_options.add_argument("window-size=1920x1080")  # 창 크기 설정
    chrome_options.add_argument("disable-gpu")  # GPU 가속 사용 안함
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 사용 안함
    chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 안함

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(f"https://search.naver.com/search.naver?where=news&query={query}")

    # 페이지 소스 가져오기 전에 스크롤 다운 로직 추가
    scroll_limit = 1
    scroll_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 로딩 대기
        scroll_count += 1  # 무한 스크롤 방지를 위해 스크롤 횟수 설정
        if scroll_count >= scroll_limit:
            break

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('li', {'class': 'bx'})
    result = []
    for article in articles:
        news_wrap = article.find('div', {'class': 'news_wrap api_ani_send'})
        if news_wrap:
            title_tag = news_wrap.find('a', {'class': 'news_tit'})
            title = title_tag.get_text(strip=True) if title_tag else "No Title"
            link = title_tag['href'] if title_tag else "No Link"

            image = "No Image"
            image_tags = news_wrap.find_all('img')
            for img in image_tags:
                if img.parent.name != 'span' and img.has_attr('src'):
                    src = img['src']
                    if not src.startswith('data:image/gif'):  # 'data:image/gif'로 시작하지 않는 이미지만 처리
                        image = src
                        break
            else:
                image = "No Image"  # 조건을 만족하는 img 태그가 없는 경우

            if image != "No Image" and not image.startswith('data:image/gif'):
                result.append({'title': title, 'link': link, 'image': image})

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
