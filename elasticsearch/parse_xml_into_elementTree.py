### value 안의 XML 형식을 파싱해 텍스트만 추출하는 과정
import xml.etree.ElementTree as ET
import requests
import time


# api 호출하여 데이터 로드하는 함수
def get_api_data(page_no, num_of_rows):
    decoding = "zfWjn+ycQoM3yTDv236ejVl8OYIfei59LxaP6xfSo20wKHhuRA4YUJIgGX1qSVQDxQiyKU++TL2HOrszC5bgCw=="

    # url : 내가 신청한 api는 3가지 서비스를 제공하고 있어서 endpoint 뒤에 의약품 제품 허가 상세정보에 관한 경로를 추가해줬음
    url = "https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService04/getDrugPrdtPrmsnDtlInq03"
    params = {'serviceKey': decoding, 'pageNo': page_no, 'numOfRows': num_of_rows, 'type': 'json'}

    # api 요청 실패 했을 때, 최대 10번까지 재시도 요청
    for _ in range(10):
        # url을 통한 정보 요청
        response = requests.get(url, params=params)
        try:
            # json() : json 형식으로 로드하는 것. text를 사용했을 때는 문자열로 인식하기 때문에 json() 파싱 방법을 이용할 거라 json()으로 사용함.
            json_data = response.json()
            return json_data
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            time.sleep(2)  # 재시도 간격만큼 대기

    print("Maximum retries reached. Returning None.")
    return None


# value 안에 있는 XML 파싱하기
def parse_doc_data(title, json_data):
    text = ''
    combined_text = []

    # 1. 주어진 데이터에서 DOC_DATA 추출
    doc_data = json_data['body']['items'][0][title]
    if doc_data:
        # 2. XML 파싱
        root = ET.fromstring(doc_data)

        # 3. ARTICLE 태그 내의 title과 해당 텍스트 추출
        articles = root.findall(".//ARTICLE")
        for article in articles:  # articles의 개수만큼 순환
            title = article.get("title")  # ARTICLE의 title 요소의 값을 추출
            paragraphs = article.findall(".//PARAGRAPH")  # ARTICLE 하위 요소인 PARAGRAPH를 전부 추출

            # 4. PARIGRAPH의 marginLeft 요소의 값에 따라 개행문자 추가 (들여쓰기를 위함)
            if title == "":  # ARTICLE의 title = "" 이면, (ARTICLE이 없는 경우)
                for paragraph in paragraphs:  # paragraphs의 개수만큼 순환
                    text += f'{paragraph.text}\n' # ARTICLE이 없기 때문에 줄바꿈 하지 않고 바로 text 출력
            else:
                for paragraph in paragraphs:
                    marginLeft_value = paragraph.get("marginLeft")  # PARAGRAPH의 marginLeft 요소의 값을 추출
                    if marginLeft_value and marginLeft_value != "0":  # 만약 그 값이 "0"이 아니면 margin 값을 줘야 하므로 들여쓰기 추가
                        text += f'\n\t\t{paragraph.text}' # ARTICLE이 있기 때문에 줄바꿈을 하고 text 출력해야 함
                    else:
                        text += f'\n\t{paragraph.text}'

            # title의 값 존재 여부에 따른 문자열 저장
            if title == "":
                combined_text.append(text)  # 한개의 ARTICLE 단위 하나로 만듦
            else:
                combined_text.append(f"{title}\t{text}")  # 한개의 ARTICLE 단위 기준으로 하나의 문자열로 저장
            text = ''

        # 전체 ARTICLE 하나의 문자열로 반환
        return '\n'.join(combined_text)
    else:
        return ""