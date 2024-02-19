# 파이어베이스에 로컬 디렉토리에 있는 파일 업로드
import firebase_admin
from firebase_admin import credentials, storage
import pandas as pd
import requests
import os
import datetime

import urllib.parse


# 파이어베이스 서비스 계정 키 다운로드한 JSON 파일 경로
cred = credentials.Certificate(r"C:\dev\hope_project\hopeimage-74788-firebase-adminsdk-qxan6-dc45fd4c42.json")

# 파이어베이스 앱 초기화
firebase_admin.initialize_app(cred, {
    'storageBucket': r'hopeimage-74788.appspot.com' # gs:// 이후 경로부터 작성
})

# 업로드할 로컬 디렉토리 경로
local_directory = r"C:\dev\hope_project\medical_dataset\image"


# 이미지 다운로드
def download_image():
    # 이미지 링크가 있는 xlsx 파일 경로
    df = pd.read_excel(r"C:\dev\hope_project\medical_dataset\medicine_image.xlsx")

    for idx, row in df.iterrows():
        code = row['ITEM_SEQ']
        img = row['ITEM_IMAGE']
        if img != '':
            response = requests.get(img)
            with open(f"C:\dev\hope_project\medical_dataset\image\img_{code}.jpg", 'wb') as f:
                f.write(response.content)

            print(f"{idx} rows processed")

# Firebase Storage에 이미지 업로드 함수
def upload_images_to_firebase(local_directory):

    # 로컬 디렉토리 내의 모든 .jpg 파일 목록 가져와서 리스트에 저장
    image_files = [f for f in os.listdir(local_directory) if f.lower().endswith('.jpg')]

    # Firebase Storage에 업로드 (파일 하나씩 순회하면서 로컬의 파일 경로 만들기 (로컬 디렉토리 + 파일 이름))
    for image_file in image_files:
        local_file_path = os.path.join(local_directory, image_file)

        # 이미지 업로드 함수 호출 (로컬의 파일 경로, 파일 이름)
        upload_image(local_file_path, image_file)

# 이미지를 업로드
def upload_image(local_file_path, image_file):
    # Firebase Storage의 blob 생성 (파일을 담을 객체)
    blob = storage.bucket().blob(image_file)
    # 해당 객체에 local_file_path로부터 데이터를 읽어와 파이어베이스에 업로드
    blob.upload_from_filename(local_file_path)
    print(f"Uploaded {local_file_path} to {image_file}")

    ## 즉, 파일 이름으로 된 blob 객체를 만들고, 로컬 경로에서 파일을 읽어와 해당 객체에 담아 업로드하는 것.

# 파이어베이스의 이미지 url 추출
def download_image_url():
    # 스토리지 버킷과 객체(파일) 목록 가져오기
    bucket = storage.bucket()
    blobs = bucket.list_blobs()

    # 데이터프레임 생성
    data = {'code': [], 'path': []}

    # 각 객체(파일)의 경로를 데이터프레임에 추가
    for i, blob in enumerate(blobs):
        # 파일 이름에서 '{code}'만 추출
        code = blob.name.replace('img_', '').replace('.jpg', '')
        path = fr"https://firebasestorage.googleapis.com/v0/b/hopeimage-74788.appspot.com/o/{blob.name}?alt=media"
        # 만료 기간을 초 단위로 설정하여 서명된 URL 생성

        data['code'].append(code)
        data['path'].append(path)

        if(i + 1) % 100 == 0:
            print(f"Processed {i + 1} blobs")

    # 데이터프레임 생성
    df = pd.DataFrame(data)

    # 합친 데이터프레임 xlsx 파일로 저장
    writer = pd.ExcelWriter(fr"C:\dev\hope_project\medical_dataset\image_paths.xlsx", options={'strings_to_urls': False})
    df.to_excel(writer, index=False)
    writer.save()

download_image_url()

    # 데이터프레임을 엑셀 파일로 저장
    # df.to_excel('image_paths.xlsx', index=False)
