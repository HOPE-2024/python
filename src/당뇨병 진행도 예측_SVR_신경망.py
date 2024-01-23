import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

# 데이터 세트 불러오기
df = pd.read_csv("https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt", sep="\t")

# S1~S6의 평균값 계산
s1_mean = df['S1'].mean()
s2_mean = df['S2'].mean()
s3_mean = df['S3'].mean()
s4_mean = df['S4'].mean()
s5_mean = df['S5'].mean()
s6_mean = df['S6'].mean()

# 데이터 세트 분리
input_features = df.iloc[:, :-1].values
output_target = df.iloc[:, -1].values

# 훈련 세트와 테스트 세트 분할
train_input, test_input, train_output, test_output = train_test_split(input_features, output_target, test_size=0.2, random_state=42)

# 서포트 벡터 머신 회귀 모델 생성 및 훈련
svr = SVR()
svr.fit(train_input, train_output)

# 신경망 모델 생성 및 훈련
nn = MLPRegressor(max_iter=1000)
nn.fit(train_input, train_output)

# 서포트 벡터 머신 회귀 모델 평가
svr_predictions = svr.predict(test_input)
svr_mse = mean_squared_error(test_output, svr_predictions)
svr_correlation = np.corrcoef(svr_predictions, test_output)[0, 1]

# 신경망 모델 평가
nn_predictions = nn.predict(test_input)
nn_mse = mean_squared_error(test_output, nn_predictions)
nn_correlation = np.corrcoef(nn_predictions, test_output)[0, 1]

# 결과 출력
print("Support Vector Machine Regressor:")
print("MSE:", svr_mse)
print("Correlation Coefficient:", svr_correlation)

print("\nNeural Network:")
print("MSE:", nn_mse)
print("Correlation Coefficient:", nn_correlation)

# 사용자 데이터 배열 변환 및 예측
user_data = np.array([[30, 1, 22, 100, s1_mean, s2_mean, s3_mean, s4_mean, s5_mean, s6_mean]])

# 각 모델에 대한 사용자 데이터 예측
svr_result = svr.predict(user_data)[0]
nn_result = nn.predict(user_data)[0]

# 예측 결과 출력
print("\nSVR 예측된 1년 후의 당뇨병 진행도:", svr_result)
print("NN 예측된 1년 후의 당뇨병 진행도:", nn_result)
