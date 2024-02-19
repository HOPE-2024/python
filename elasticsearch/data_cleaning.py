# 데이터 정제 (추후에 다른 함수들과 연관지어야 함, api에 자동으로 데이터 들어왔을 때 엘라스틱 서치에 추가되어야 하기 때문)
import pandas as pd

# 엑셀 파일의 url 저장
file_url = r"C:\dev\hope_project\medical_dataset\medicine_9th.xlsx"

# xlsx 파일을 읽어서 데이터프레임 생성
df = pd.read_excel(file_url)

# 데이터 프레임의 각 열에 존재하는 널 값의 개수 출력
print(df.isnull().sum())
# 결측치 수정하기 -> 모든 널값을 "-"로 변경
change_null_data = df.fillna("https://firebasestorage.googleapis.com/v0/b/hopeimage2.appspot.com/o/img_noimage.jpg?alt=media")
print(change_null_data.isnull().sum())

# xlsx 파일로 저장
writer = pd.ExcelWriter(r"C:\dev\hope_project\medical_dataset\medicine_11th.xlsx", options={'strings_to_urls': False})
change_null_data.to_excel(writer, index=False)
writer.save()