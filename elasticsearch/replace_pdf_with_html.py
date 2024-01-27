### url 변환하는 과정(pdf -> html). 변환 후, 기존 열의 값을 새 값으로 바꿔치기 한 후 새로운 파일로 저장
import pandas as pd

# 엑셀 파일의 url 저장
file_url = r"C:\dev\medical_dataset\medical_1st.xls"

# xlsx 파일을 읽어서 데이터프레임 생성
df = pd.read_excel(file_url)

# effect, usages, precautions 열에서 값이 존재하는 행 선택
# notna() : 공백이 있으면 false, 없으면 true 반환
valid_rows = df[['effect', 'usages', 'precautions']].notna()

# 선택된 행에 대해 URL 생성 (예시로 'effect' 열에 대한 URL 생성)
urls_effect = df.loc[valid_rows['effect'], 'code'].apply(lambda x: f"https://nedrug.mfds.go.kr/pbp/cmn/html/{x}/EE")
# 선택된 행에 대해 URL 생성 (예시로 'usages' 열에 대한 URL 생성)
urls_usages = df.loc[valid_rows['usages'], 'code'].apply(lambda x: f"https://nedrug.mfds.go.kr/pbp/cmn/html/{x}/UD")
# 선택된 행에 대해 URL 생성 (예시로 'precautions' 열에 대한 URL 생성)
urls_precautions = df.loc[valid_rows['precautions'], 'code'].apply(lambda x: f"https://nedrug.mfds.go.kr/pbp/cmn/html/{x}/NB")

# 새로운 URL 값을 기존 열에 추가 (바꿔치기)
df.loc[valid_rows['effect'], 'effect'] = urls_effect
df.loc[valid_rows['usages'], 'usages'] = urls_usages
df.loc[valid_rows['precautions'], 'precautions'] = urls_precautions

# xlsx 파일로 저장
writer = pd.ExcelWriter(r"C:\dev\medical_dataset\medical_datasets\medical_2nd.xlsx", options={'strings_to_urls': False})
df.to_excel(writer, index=False)
writer.save()




##### 3개의 열에 대한 모든 링크를 수정해야 하는데 한번에 하려고 하면 길이 초과 오류가 떠서 데이터가 정상적으로 들어오지 않음.
##### 따라서 번거롭더라도 나눠서 진행함. 아래는 한번에 진행하는 한 번에 수정하는 코드.
####### 수정) 나눠서 진행하려고 했는데 일이 너무 번거로워져서 찾아본 결과, 길이 제한 오류는 한 워크시트에 url을 많이 쓰려고 했을 경우에 발생!! 따라서 url이 아닌, 일반 문자열로 저장되도록 코드 수정

# 기존 저장 코드
# df.to_excel(r"C:\dev\medical_dataset\medical_datasets\medical_2_1_2.xlsx", index=False)

# 수정 저장 코드
# writer = pd.ExcelWriter(r"C:\dev\medical_dataset\medical_datasets\medical_2nd.xlsx", engine_kwargs={'strings_to_urls': False})
# df.to_excel(writer, index=False)
# writer.save()


####################### 만약, 한 개의 열만 수정하고 싶다면

# # 엑셀 파일의 url 저장
# file_url = r"C:\dev\medical_dataset\medical_1st.xls"
#
# # xlsx 파일을 읽어서 데이터프레임 생성
# df = pd.read_excel(file_url)
#
# # effect, usages, precautions 열에서 값이 존재하는 행 선택
# # notna() : 공백이 있으면 false, 없으면 true 반환
# # all(axis=1) : 한 행이 모두 true인 행만 선택
# valid_rows = df['effect'].notna()
#
# # 선택된 행에 대해 URL 생성
# urls = df.loc[valid_rows, 'code'].apply(lambda x: f"https://nedrug.mfds.go.kr/pbp/cmn/html/{x}/EE")
#
# # URL 값을 새로운 열에 추가
# df.loc[valid_rows, 'effect'] = urls
#
# # 새로운 xlsx 파일로 저장
# writer = pd.ExcelWriter(r"C:\dev\medical_dataset\medical_datasets\medical_2nd.xlsx", engine_kwargs={'strings_to_urls': False})
# df.to_excel(writer, index=False)
# writer.save()