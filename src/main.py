import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

import 기대_수명_예측
import 당뇨병_진행도_예측_랜덤_포레스트
import 연도별_국가_평균_수명_시각화
import 머신_러닝으로_얼굴_인식_후_성별_나이_출력

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

# 아래 경로로 요청이 들어올때 해당 함수를 실행
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
    prediction,feature_importances, correlation, correlation_x, correlation_y = 기대_수명_예측.predict_life_expectancy(year, bmi, alcohol, country)

    # JSON 형태로 결과 반환
    return jsonify({
        'prediction': prediction, # 기대 수명
        'feature_importances': feature_importances, # 특성 중요도
        'correlation': correlation, # 상관 계수
        'correlation_x' : correlation_x,
        'correlation_y' : correlation_y
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
    prediction,feature_importances, correlation, correlation_x, correlation_y = 당뇨병_진행도_예측_랜덤_포레스트.diabetes_Random(age, bmi, bp, gender)

    # JSON 형태로 결과 반환
    return jsonify({
        'prediction': prediction, # 기대 수명
        'feature_importances': feature_importances, # 특성 중요도
        'correlation': correlation, # 상관 계수
        'correlation_x' : correlation_x,
        'correlation_y' : correlation_y
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
        print("검출 결과")
        print(results)
        return jsonify({'results': results})

    return jsonify({'error': 'Unknown error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
