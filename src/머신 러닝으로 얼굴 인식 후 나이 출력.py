import cv2
import numpy as np
import subprocess

# 얼굴 인식을 위한 캐스케이드 분류기 로드
face_cascade = cv2.CascadeClassifier('../opencv/haarcascade_frontalface_default.xml')

# 안면 나이 추정 및 성별 추정을 위한 딥러닝 모델 로드
age_model = cv2.dnn.readNetFromCaffe('../opencv/age_deploy.prototxt', '../opencv/age_net.caffemodel')
gender_model = cv2.dnn.readNetFromCaffe('../opencv/gender_deploy.prototxt', '../opencv/gender_net.caffemodel')

# 연령 및 성별 리스트 정의
age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
gender_list = ['Male', 'Female']
age_mid = [1, 5, 10, 17.5, 28.5, 40.5, 50.5, 80]

# 이미지 파일 읽기
img = cv2.imread('../data/two.JPG')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 얼굴 검출
# scaleFactor: 이미지 크기를 줄이는 비율을 결정, 이 값이 크면 더 많은 얼굴을 빠르게 검출할 수 있지만 정확도는 감소
# minNeighbors: 검출된 얼굴 후보가 유효한 것으로 간주되기 위해 가지고 있어야 하는 이웃 수를 결정, 이 값이 높을수록 더 많은 품질의 얼굴을 검출할 수 있지만, 얼굴 검출 수는 감소
faces = face_cascade.detectMultiScale(gray, 1.3, 5) #

# ========================================
# for (x, y, w, h) in faces: # 이미지에 얼굴 위치 표시
# 	cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#
# cv2.imshow('Face Detection Check', img) # 수정된 이미지 표시
# ========================================


if len(faces) == 0:
    # Haar Cascade로 얼굴을 검출하지 못한 경우, 딥러닝 기반 얼굴 검출 스크립트 실행
    subprocess.run(["python", "딥러닝으로 얼굴 인식 후 나이 출력.py"])
else:
    # 각 얼굴에 대한 처리
    for (x, y, w, h) in faces:
        face_img = img[y:y + h, x:x + w]
        blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

        # 나이 추정
        age_model.setInput(blob)
        age_preds = age_model.forward()
        age = age_list[age_preds[0].argmax()]
        age_est = round(np.sum(age_mid * age_preds[0]))  # 나이 추정 결과를 계산하고 반올림

        # 성별 추정
        gender_model.setInput(blob)
        gender_preds = gender_model.forward()  # squeeze() 시 오히려 성별을 다르게 추정
        gender = gender_list[gender_preds[0].argmax()]

        # 결과 출력
        label = f'{gender}, {str(age_est)}, {age}'
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
    # 이미지 표시
    cv2.imshow('Gender and Age Detection', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
