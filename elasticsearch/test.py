import os
import time

file_path = 'extract_json_data.py'  # 생성 날짜를 확인하려는 파일 경로

if os.path.exists(file_path):
    file_stat = os.stat(file_path)
    created_timestamp = file_stat.st_ctime
    created_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created_timestamp))
    print(f"파일 생성 날짜: {created_date}")  # 파일 생성 날짜: 2023-09-16 19:55:34
else:
    print("파일이 존재하지 않습니다.")
