# 최종적으로, 두개로 나눠진 엑셀 파일을 불러 두 데이터프레임에 담고, 하나의 파일로 합치는 코드
import pandas as pd

# 두개의 데이터프레임 생성
df1 = pd.read_excel(r"C:\dev\medical_dataset\medicine_5th.xlsx")
df2 = pd.read_excel(r"C:\dev\medical_dataset\medicine_6th.xlsx")

# 두 데이터프레임을 열을 기준으로 오른쪽으로 합치기
merged_df = pd.concat([df1, df2], axis=1)

# 합친 데이터프레임 xlsx 파일로 저장
writer = pd.ExcelWriter(fr"C:\dev\medical_dataset\medicine_7th.xlsx", options={'strings_to_urls': False})
merged_df.to_excel(writer, index=False)
writer.save()
print(merged_df)
