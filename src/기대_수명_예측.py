import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# import matplotlib.pyplot as plt

def predict_life_expectancy(year, bmi, alcohol, country):
    # 데이터 준비
    data = pd.read_csv('../data/Life Expectancy Data.csv')
    data = data.drop(columns=['Status'])  # 모델 학습에 필요없다고 판단되는 'Status' 열 제거

    # 수치형 데이터의 결측치를 평균으로 채우기
    data.fillna(data.mean(numeric_only=True), inplace=True)

    # 결측치 처리 후 데이터 확인 : 각 열별 결측치의 개수를 확인 가능하며, 0 이면 결측치가 존재하지 않는 것이다.
    # data.isnull().sum()

    # 국가별 평균 계산 (Year, BMI, Alcohol을 제외한 나머지 특성에 대해)
    country_averages = data.groupby('Country').mean(numeric_only=True)
    average_bmi = country_averages.loc[country, 'BMI']
    average_alcohol = country_averages.loc[country, 'Alcohol']

    # 'Country', 'Year', 'BMI', 'Alcohol', 'Life expectancy' 을 제외한 나머지 특성에 대한 국가별 평균을 저장
    country_averages = country_averages.drop(columns=['Year', 'Life expectancy'])

    # "목표 변수 = 예측할 값" 설정
    target = data['Life expectancy']

    # 특성 선택 및 전처리 (Country 제외)
    features = data.drop(columns=['Country', 'Life expectancy'])

    # 표준화 전에 열 이름 저장
    feature_names = features.columns

    # 표준화
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    # 데이터 분할
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2)

    # 모델 구축 및 훈련
    # model = RandomForestRegressor(n_estimators=100, random_state=42)
    model = RandomForestRegressor(max_depth=4)
    model.fit(x_train, y_train)

    # 모델 평가 (1) : 상관 계수
    predictions = model.predict(x_test)
    actual_values = y_test
    correlation = np.corrcoef(predictions, actual_values)
    print("Correlation Coefficient:", correlation)

    # 상관 계수 시각화 → 리액트 시각화
    # plt.scatter(predictions, actual_values)
    # plt.xlabel('Predicted Values')
    # plt.ylabel('Actual Values')
    # plt.title('Correlation between Predictions and Actual Values')
    # plt.show()

    # 모델 평가 (2) : 평균 제곱 오차
    predictions = model.predict(x_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

    # 사용자 입력
    user_input = {'Year': year, 'BMI': bmi, 'Alcohol': alcohol, 'Country': country}
    # display(country_averages.columns)

    # 미리 저장해 놓았던 국가별 평균값 추가
    for feature in country_averages.columns:
        user_input[feature] = country_averages.loc[user_input['Country'], feature]

    # 'Country' 제외
    user_input.pop('Country')
    # display(user_input)

    # DataFrame으로 변환하면서 feature_names 순서에 맞게 정렬
    user_input_df = pd.DataFrame([user_input])[feature_names]
    print(user_input_df)

    # 표준화
    user_input_scaled = scaler.transform(user_input_df)

    # 예측 수행
    predicted_life_expectancy = model.predict(user_input_scaled)

    # 특성 중요도 확인
    importance = model.feature_importances_

    # 특성 이름과 중요도를 사전 형태로 매핑
    importance_dict = dict(zip(feature_names, importance))

    # 특성 중요도를 내림차순으로 정렬
    sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

    # 정렬된 특성 중요도를 출력
    for feature, importance in sorted_importance:
        print(f"{feature} 중요도: {importance}")

    # 특성 이름과 중요도를 분리
    features = [item[0] for item in sorted_importance]
    importances = [item[1] for item in sorted_importance]

    # 막대 그래프 그리기 → 리액트 시각화
    # plt.figure(figsize=(10, 8))
    # plt.barh(features, importances, color='skyblue')
    # plt.xlabel("Expected life expectancy predictors")
    # plt.title("Feature Importance")
    # plt.gca().invert_yaxis()
    # plt.show()

    # 기대 수명, 특성 중요도, 상관 계수 반환, bmi, alcohol
    return predicted_life_expectancy[
        0], sorted_importance, correlation.tolist(), predictions.tolist(), actual_values.tolist(), average_bmi, alcohol, average_alcohol
