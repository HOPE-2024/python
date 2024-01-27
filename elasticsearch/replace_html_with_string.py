### html url을 크롤링하여 문자만 추출하는 과정
import pandas as pd
from urllib.request import urlretrieve # 파이썬에서 url을 다루기 위한 모듈
from bs4 import BeautifulSoup

# 데이터프레임을 나눌 크기를 지정 (한꺼번에 많은 내용 저장하면 오류날 가능성 높아 나눠서 저장)
chunk_size = 100

# xlsx 파일로 데이터프레임 생성
df = pd.read_excel(r"C:\dev\medical_dataset\medical_datasets\medical_2nd.xlsx")

# 데이터프레임을 나누어 처리
for i in range(0, len(df), chunk_size):
    chunk_df = df.iloc[i:i+chunk_size]
    for index, row in chunk_df.iterrows():
        for column in ["effect", "usages", "precautions"]:
            url = row[column]
            if pd.notna(url):
                html_file = f"{column}_{index}.html"
                try:
                    urlretrieve(url, html_file)
                except Exception as e:
                    print(f"error downloading {url}: {e}")
                    continue
                with open(html_file, "r", encoding="utf-8") as f:
                    html = f.read()
                soup = BeautifulSoup(html, "html.parser")
                # "h1" 태그와 "p" 태그를 이용하여 내용을 추출
                content_tag = soup.find("h1")
                if content_tag:
                    content = content_tag.get_text() + "\n"
                    content_tags = soup.find_all("p", class_="indent0")
                    for tag in content_tags:
                        content += " - " + tag.get_text() + "\n"
                else:
                    content = ""
                df.loc[index, column] = content
    # 처리한 데이터 프레임을 엑셀 파일로 저장
    writer = pd.ExcelWriter(f"C:\\dev\\medical_dataset\\medical_datasets\\medicine_{i}.xlsx", engine='xlsxwriter',
                            options={'strings_to_urls': False})
    chunk_df.to_excel(writer, index=False)
    writer.save()