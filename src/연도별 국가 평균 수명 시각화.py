import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 읽기
df = pd.read_csv('../data/Country Avarage Life Expectancy.csv')

print(df.head())

# 연도별 데이터 선택
years = df.columns[4:]  # 첫 4개 열을 제외한 연도 데이터

# 특정 나라를 위한 데이터 선택, 예를 들어 'South Korea'
country = 'Korea, Rep.'
data = df[df['Country Name'] == country].iloc[0][years]

# 꺾은선 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(years, data, marker='o')  # 꺾은선 그래프 그리기
plt.title(f'Life Expectancy in {country} Over the Years')
plt.xlabel('Year')
plt.ylabel('Life Expectancy')
plt.xticks(rotation=45)  # x축 레이블 회전
plt.grid(True)
plt.show()
