from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
# from sklearn.svm import SVR
# from sklearn.neural_network import MLPRegressor
# from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
import pandas as pd


def predict_future(country, year):
	# 데이터 불러오기
	file_path = '../data/Country Avarage Life Expectancy.csv'
	data = pd.read_csv(file_path)

	# 필요하지 않은 컬럼 제거
	data_cleaned = data.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])

	# 데이터를 '나라', '연도', '기대 수명' 형태로 변환
	data_melted = data_cleaned.melt(id_vars=['Country Name'], var_name='Year', value_name='Life Expectancy')

	# 결측치 처리
	data_melted['Life Expectancy'] = data_melted.groupby('Country Name')['Life Expectancy'].transform(
		lambda x: x.fillna(x.mean()))
	data_final = data_melted.dropna()

	# '나라' 컬럼을 원 핫 인코딩 → 해당 나라일때는 1, 나머지 나라는 전부 0
	# '연도'는 수치형으로 그대로 사용
	# PCA (차원의 저주를 예방하기 위한 차원 축소) 적용을 위해 표준화 추가
	preprocessor = ColumnTransformer(
		transformers=[
			('num', 'passthrough', ['Year']),
			('cat', OneHotEncoder(), ['Country Name'])
		],
		remainder='drop'
	)

	# 표준화 및 PCA 적용
	pipeline = make_pipeline(
		preprocessor,
		StandardScaler(with_mean=False),  # OneHotEncoder 후에는 with_mean=False 설정이 필요할 수 있기에
		PCA(n_components=0.95)  # 설명된 분산의 95%를 유지
	)

	# 데이터 분할
	X = data_final[['Country Name', 'Year']]
	y = data_final['Life Expectancy'].astype(float)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

	# 모델 초기화 및 학습, 평가 (Random Forest만 사용)
	# 랜덤 포레스트 모델이 가장 평가가 좋았지만, 랜덤 포레스트 모델은 외삽에 취약 →
	models = {
		# "Random Forest": make_pipeline(preprocessor, RandomForestRegressor(random_state=42)),
		"Linear Regression": make_pipeline(preprocessor, LinearRegression()),
		# "SVM": make_pipeline(preprocessor, SVR()),
		# "Neural Network": make_pipeline(preprocessor, MLPRegressor(random_state=42)),
		# "Gradient Boosting": make_pipeline(preprocessor, GradientBoostingRegressor(random_state=42))
	}

	scores = {}
	for model_name, model in models.items():
		model.fit(X_train, y_train)
		predictions = model.predict(X_test)
		scores[model_name] = mean_squared_error(y_test, predictions, squared=False)  # RMSE

	# 평균 제곱근 오차 출력, 해당 값이 작을수록 모델의 성능이 우수
	# for model_name, rmse in scores.items():
	#     print(f"{model_name} : {rmse}")

	# 가장 성능이 좋은 모델 선택 (이 경우 Random Forest만 사용)
	best_model_name = min(scores, key=scores.get)
	best_model = models[best_model_name]
	print(f"\n모델의 이름과 평가 : {best_model_name}, {scores[best_model_name]}")

	# 예측 결과 출력
	prediction = best_model.predict(pd.DataFrame([[country, year]], columns=['Country Name', 'Year']))
	print(f"\nThe predicted life expectancy in {country} in {year} is {prediction[0]}")

	return prediction[0]
