# 나눠서 저장한 엑셀 파일을 하나로 합치는 코드(병합)
import pandas as pd
import glob

# 병합할 파일 경로와 파일 이름 패턴을 지정
path = r"C:/dev/medical_dataset"
pattern = 'medicine_4th*.xlsx'  # * 앞의 경로로 시작하는 파일들

# 모든 파일을 읽어와서 데이터프레임 리스트에 추가
df_list = []
for filename in glob.glob(f"{path}/{pattern}"):  # 지정된 패턴에 맞는 모든 파일의 경로를 가져옴
    df_list.append(pd.read_excel(filename))  # 각 파일을 읽어서 데이터프레임으로 저장
    print(filename)

# 데이터프레임 리스트를 하나로 합침
merged_df = pd.concat(df_list, ignore_index=True)

# 합친 데이터프레임 xlsx 파일로 저장
writer = pd.ExcelWriter(fr"C:\dev\medical_dataset\medicine_6th.xlsx", options={'strings_to_urls': False})
merged_df.to_excel(writer, index=False)
writer.save()

# append() : 하나의 데이터프레임에 다른 데이터프레임을 하나씩 추가하는 DataFrame 객체의 메서드.
# concat() : 여러 개의 데이터프레임을 한 번에 결합하는 pandas의 함수. axis = 0은 열, axis = 1은 행을 기준으로 병합