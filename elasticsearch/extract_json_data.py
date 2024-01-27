# api로부터 받아온 json 데이터의 원하는 값만 추출하는 코드

import requests
import pandas as pd
from parse_xml_into_elementTree import get_api_data

pageNo = 1
numOfRows = 100
chunk_size = 100
# 추출한 데이터를 DataFrame으로 변환 (리스트가 한 데이터프레임에 저장됨)
df = pd.DataFrame()
data_to_save = []

# 한 페이지당 100개의 결과 띄우고 마지막페이지까지 순회
for i in range(0, 483):  # 483
    # API로부터 JSON 데이터 가져오기
    json_data = get_api_data(pageNo, numOfRows)  # 한번에 100개의 정보가 넘어옴
    # 추출하고자 하는 키들 지정
    selected_keys = ['ITEM_SEQ', 'ITEM_NAME', 'ITEM_ENG_NAME', 'ENTP_NAME', 'ENTP_ENG_NAME', 'ETC_OTC_CODE', 'CHART', 'MAIN_ITEM_INGR', 'MAIN_INGR_ENG', 'STORAGE_METHOD', 'VALID_TERM', 'EDI_CODE', 'INGR_NAME', 'INSERT_FILE']

    # 각 item 요소들을 순회하며 선택한 키들에 대한 값 추출하여 리스트로 저장
    data_to_save = [{key: item[key] for key in selected_keys} for item in json_data['body']['items']]

    # data_to_save를 데이터프레임으로 변환하고, 기존 df에 추가하여 저장
    df = pd.concat([df, pd.DataFrame(data_to_save)], ignore_index=True)

    # 다음 반복문 진입 시에 data_to_save가 널 값이어야 df에 추가할 때 중복이 생기지 않음
    data_to_save = []
    pageNo += 1
    print("페이지 번호 : ", pageNo)

excel_file_path = r"C:\dev\medical_dataset\medicine_datasets\medicine_test.xlsx"
df.to_excel(excel_file_path, index=False)