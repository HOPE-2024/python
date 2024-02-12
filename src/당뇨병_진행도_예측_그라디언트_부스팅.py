import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

# 링크하신 데이터 세트를 불러옵니다.
df = pd.read_csv("https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt", sep="\t")

# S1~S6의 평균값 계산 후 변수에 저장
s1_mean = df['S1'].mean()
s2_mean = df['S2'].mean()
s3_mean = df['S3'].mean()
s4_mean = df['S4'].mean()
s5_mean = df['S5'].mean()
s6_mean = df['S6'].mean()

# 데이터 세트를 입력 변수와 목표 변수로 분리
input_features = df.iloc[:, :-1].values
output_target = df.iloc[:, -1].values

# 데이터를 훈련 세트와 테스트 세트로 분할
train_input, test_input, train_output, test_output = train_test_split(input_features, output_target, test_size=0.2, random_state=42)

# 그라디언트 부스팅 회귀 모델을 생성 후 훈련
GBR = GradientBoostingRegressor(max_depth=5)
GBR.fit(train_input, train_output)

# 모델 평가 : 상관 계수
predictions = GBR.predict(test_input)
actual_values = test_output
correlation = np.corrcoef(predictions, actual_values)
print("Correlation Coefficient:", correlation)

# 상관 계수 시각화
plt.scatter(predictions, actual_values)
plt.xlabel('Predicted Values')
plt.ylabel('Actual Values')
plt.title('Correlation between Predictions and Actual Values')
plt.show()

# Mean Squared Error (MSE)를 계산합니다.
MSE = mean_squared_error(test_output, GBR.predict(test_input))
print("Mean Squared Error (MSE):", MSE)

# NMSE
NMSE=MSE/np.max(test_output)
print("Normalized Mean Squared Error (MSE):", NMSE)

# 사용자 데이터를 배열로 변환
user_data = np.array([[30,  # age
                       1,   # sex
                       22,  # bmi
                       100, # bp
                       s1_mean, # s1
                       s2_mean, # s2
                       s3_mean,  # s3
                       s4_mean, # s4
                       s5_mean, # s5
                       s6_mean  # s6
                      ]])

# 모델을 사용하여 예측 수행
predicted_degree = GBR.predict(user_data)

# 예측 결과 출력
result = predicted_degree[0]
print("예측된 1년 후의 당뇨병 진행도 : ", result)

# 특성 중요도 확인
importance = GBR.feature_importances_

# 특성 이름과 중요도를 사전 형태로 매핑
importance_dict = dict(zip(df.columns[:-1], importance))

# 특성 중요도를 내림차순으로 정렬
sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

# 정렬된 특성 중요도를 출력
for feature, importance in sorted_importance:
    print(f"{feature} 중요도: {importance}")

# 특성 중요도를 시각화
plt.figure(figsize=(10, 8))
sorted_features = [item[0] for item in sorted_importance]
sorted_importances = [item[1] for item in sorted_importance]
plt.barh(sorted_features, sorted_importances, color='skyblue')
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Feature Importances in Diabetes Model")
plt.gca().invert_yaxis()
plt.show()
