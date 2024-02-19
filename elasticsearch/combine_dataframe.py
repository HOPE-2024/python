# 최종적으로, 두개로 나눠진 엑셀 파일을 불러 두 데이터프레임에 담고, 하나의 파일로 합치는 코드
import pandas as pd

# 두개의 데이터프레임 생성
df_ver1 = pd.read_excel(r"C:\dev\hope_project\medical_dataset\medicine_8th.xlsx")
df_ver2 = pd.read_excel(r"C:\dev\hope_project\medical_dataset\image_paths3.xlsx")


def combine_dataframe_concat(df1, df2):
    # 두 데이터프레임을 열을 기준으로 오른쪽으로 합치기
    # axis=0 : 행간 결합 , axis=1 : 열간 결합
    merged_df = pd.concat([df1, df2], axis=0)

    # 합친 데이터프레임 xlsx 파일로 저장
    writer = pd.ExcelWriter(r"C:\dev\hope_project\medical_dataset\image_paths3.xlsx", options={'strings_to_urls': False})
    merged_df.to_excel(writer, index=False)
    writer.save()
    print(merged_df)


# combine_dataframe_concat(df_ver1, df_ver2)

def combine_dataframe_merge(df1, df2):
    # 두 데이터프레임을 합집합 병합하기 (데이터 보존)
    # axis=0 : 행간 결합 , axis=1 : 열간 결합
    merged_df = pd.merge(left=df1, right=df2, how="left", on="code")

    # 합친 데이터프레임 xlsx 파일로 저장
    writer = pd.ExcelWriter(r"C:\dev\hope_project\medical_dataset\medicine_9th.xlsx", options={'strings_to_urls': False})
    merged_df.to_excel(writer, index=False)
    writer.save()
    print(merged_df)


combine_dataframe_merge(df_ver1, df_ver2)

