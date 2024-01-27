import pandas as pd
import requests
import bs4
from pprint import pprint
# serviceKey
encoding = "gbdPOFUEcQhjoPzjqCMf%2FiVGvuAXiltyL8nE7U1tN9Nue5Quv8sEYKl%2B8dqhOGQ8Pk1dP%2FK5%2BvRtiMtJUzrLCQ%3D%3D"
decoding = "gbdPOFUEcQhjoPzjqCMf/iVGvuAXiltyL8nE7U1tN9Nue5Quv8sEYKl+8dqhOGQ8Pk1dP/K5+vRtiMtJUzrLCQ=="

# url : 내가 신청한 api는 3가지 서비스를 제공하고 있어서 endpoint 뒤에 의약품 제품 허가 상세정보에 관한 경로를 추가해줬음
url = "https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService04/getDrugPrdtPrmsnDtlInq03"
params = {'serviceKey': decoding, 'pageNo': '1', 'numOfRows': '1', 'type': 'json'}

# url을 통한 정보 요청
response = requests.get(url, params=params)

# 내용
content = response.json()

pprint(content)

# bs4 사용하여 item 태그 분리
xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
rows = xml_obj.find_all('item')
# print(rows)

# 컬럼 값 조회용
# columns = rows[0].find_all()
# print(columns)

# 각 행의 컬럼, 이름 값을 가지는 리스트 만들기
row_list = [] # 행(전체 행)
name_list = [] # 열 (이름)
value_list = [] # 데이터 값(셀)

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all() # item으로 구분된 데이터 => 약 하나에 대한 데이터
    # 첫째 행 데이터 수집
    for j in range(0, len(columns)):
        if i == 0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value 값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list = []

# xml 값 DataFrame으로 만들기
df = pd.DataFrame(row_list, columns=name_list)
# print(df)

# df.to_excel(r'C:\dev\medical_dataset\test.xlsx', index=False)