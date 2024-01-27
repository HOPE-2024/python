# url로 되어있는 데이터를 파싱한 텍스트로 바꾸는 과정
# xml 파싱하여 text 추출하는 함수 호출
# 1000개 단위로 나누어서 저장

import pandas as pd
from parse_xml_into_elementTree import parse_doc_data, get_api_data

# 엑셀 파일의 url 저장
file_url = r"C:\dev\medical_dataset\medicine_datasets\medicine_3type.xlsx"

# xlsx 파일을 읽어서 데이터프레임 생성
df = pd.read_excel(file_url)
chunk_size = 100


# url을 변환한 text로 바꾸기
def replace_text():
    # 0부터 데이터 프레임의 길이까지. 100씩 증가.
    for i in range(48200, 48235, chunk_size):
        # 전체 데이터프레임에서 해당 범위에 맞는 데이터만 깊은 복사
        chunk_df = df.copy().iloc[i:i+chunk_size]

        # effect, usages, precautions 열에서 값이 존재하는 행 선택
        # notna() : 공백이 있으면 false, 없으면 true 반환
        valid_rows = df[['effect', 'usages', 'precautions']].notna()
        # 첫번째 페이지 번호 초기화
        pageNo = i + 1

        # 변환한 값 담아놓을 리스트 -> 나중에 한번에 데이터프레임에 넣음
        all_urls_effect = []
        all_urls_usages = []
        all_urls_precautions = []

        # chunk_size만큼 반복문 돌며 리스트에 내용 저장
        for j in range(0, chunk_size):
            # api 호출하여 데이터 불러오는 함수
            json_data = get_api_data(pageNo, 1)
            # 해당 태그 값 파싱
            urls_effect = parse_doc_data('EE_DOC_DATA', json_data)
            urls_usages = parse_doc_data('UD_DOC_DATA', json_data)
            urls_precautions = parse_doc_data('NB_DOC_DATA', json_data)

            # 리스트에 파싱한 값 추가.
            all_urls_effect.append(urls_effect)
            all_urls_usages.append(urls_usages)
            all_urls_precautions.append(urls_precautions)

            # API 결과에 더 이상 데이터가 없으면 종료
            if json_data['body']['totalCount'] <= pageNo:
                break

            pageNo += 1
            print("페이지 번호 : ", pageNo)

        # 새로운 값 담은 리스트를 기존 열에 추가
        chunk_df.loc[valid_rows['effect'], 'effect'] = all_urls_effect
        chunk_df.loc[valid_rows['usages'], 'usages'] = all_urls_usages
        chunk_df.loc[valid_rows['precautions'], 'precautions'] = all_urls_precautions

        save_to_excel(chunk_df, (i + chunk_size))


def save_to_excel(chunk_df, end_df):
    writer = pd.ExcelWriter(fr"C:\dev\medical_dataset\medicine_datasets\medicine_{end_df}.xlsx")
    chunk_df.to_excel(writer, index=False)
    writer.save()
    print(f"excel 저장 완료 : medicine_{end_df}")


replace_text()