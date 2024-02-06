import base64

import cv2
import numpy as np
# import subprocess
import 딥러닝으로_얼굴_인식_후_성별_나이_출력

# 얼굴 인식 및 나이, 성별 추정 함수 수정
def machine_face(img):
    # 얼굴 인식을 위한 머신 러닝 기반 캐스케이드 분류기 로드
    face_cascade = cv2.CascadeClassifier('../opencv/haarcascade_frontalface_default.xml')

    # 안면 나이 추정 및 성별 추정을 위한 딥러닝 모델 로드
    age_model = cv2.dnn.readNetFromCaffe('../opencv/age_deploy.prototxt', '../opencv/age_net.caffemodel')
    gender_model = cv2.dnn.readNetFromCaffe('../opencv/gender_deploy.prototxt', '../opencv/gender_net.caffemodel')

    # 연령 및 성별 리스트 정의
    age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    gender_list = ['Male', 'Female']
    age_mid = [1, 5, 10, 17.5, 28.5, 40.5, 50.5, 80]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    results = []

    if len(faces) == 0:
        # Haar Cascade로 얼굴을 검출하지 못한 경우, 딥러닝 기반 얼굴 검출
        print("머신 러닝 모델이 얼굴 검출을 실패하여, 딥러닝 모델로 시도하겠습니다.")
        # subprocess.run(["python", "딥러닝으로_얼굴_인식_후_성별_나이_출력.py"])
        return 딥러닝으로_얼굴_인식_후_성별_나이_출력.deep_face(img)
    else:
        for (x, y, w, h) in faces:
            # 검출된 얼굴 이미지를 메모리에 저장
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            _, buffer = cv2.imencode('.png', img)
            image_bytes = base64.b64encode(buffer.tobytes()).decode('utf-8')
            
            face_img = img[y:y+h, x:x+w]
            blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

            age_model.setInput(blob)
            age_preds = age_model.forward()
            age = age_list[age_preds[0].argmax()]
            age_est = round(np.sum(age_mid * age_preds[0]))

            gender_model.setInput(blob)
            gender_preds = gender_model.forward()
            gender = gender_list[gender_preds[0].argmax()]

            label = f'{gender}, {age_est}, {age}'
            results.append(label)

            return results, image_bytes