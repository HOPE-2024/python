import cv2
import numpy as np

# 딥러닝 기반 얼굴 인식 모델 로드
facenet = cv2.dnn.readNet('../opencv/deploy.prototxt', '../opencv/res10_300x300_ssd_iter_140000.caffemodel')

# 나이 추정 및 성별 추정을 위한 딥러닝 모델 로드
age_model = cv2.dnn.readNetFromCaffe('../opencv/age_deploy.prototxt', '../opencv/age_net.caffemodel')
gender_model = cv2.dnn.readNetFromCaffe('../opencv/gender_deploy.prototxt', '../opencv/gender_net.caffemodel')

# 연령 및 성별 리스트 정의
age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
gender_list = ['Male', 'Female']
age_mid = [1, 5, 10, 17.5, 28.5, 40.5, 50.5, 80]

# 이미지 파일 읽기
img = cv2.imread('../data/face_2.JPG')

# 이미지의 높이, 너비 추출
h, w, c = img.shape

# 이미지 전처리
blob = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))

# 얼굴 영역 검출 모델에 입력
facenet.setInput(blob)
detections = facenet.forward()

detected_faces = []  # 검출된 얼굴들을 저장할 리스트
# 계속 얼굴이 아닌 부분을 얼굴로 인식하는 경우가 존재하여, 해당 문제 상황을 방지하기 위하여 검출되는 얼굴의 개수에 따라서 검출 임계점을 다르게 설정

# 모든 얼굴을 검출하고 리스트에 추가
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
        x1 = int(detections[0, 0, i, 3] * w)
        y1 = int(detections[0, 0, i, 4] * h)
        x2 = int(detections[0, 0, i, 5] * w)
        y2 = int(detections[0, 0, i, 6] * h)
        detected_faces.append((x1, y1, x2, y2, confidence))

# 얼굴의 수에 따라 임계값 조정
threshold = 0.99 if len(detected_faces) == 1 or 2 else 0.5

# 조건에 맞는 얼굴에 대한 처리
for (x1, y1, x2, y2, confidence) in detected_faces:
    if confidence >= threshold:
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        face_img = img[y1:y2, x1:x2]
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

        # 나이 추정
        age_model.setInput(blob)
        age_preds = age_model.forward()
        age_class = age_preds[0].argmax()
        age = age_list[age_class]
        age_est = round(np.sum(age_mid[age_class] * age_preds[0]))

        # 성별 추정
        gender_model.setInput(blob)  # 모델의 입력값을 선처리 데이터로 선정
        gender_preds = gender_model.forward()  # forward : 추론, squeeze : 차원 축소
        gender_class = gender_preds[0].argmax()  # argmax : 사람이 이해할 수 있게 압축
        gender = gender_list[gender_class]

        # 결과 레이블 생성 및 출력
        label = f"{gender}, {age_est}, {age}"
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# 얼굴이 검출되지 않았을 때 메시지 표시
if not detected_faces:
    cv2.putText(img, "Face Not Found", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# 결과 이미지 표시
cv2.imshow('Face Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
