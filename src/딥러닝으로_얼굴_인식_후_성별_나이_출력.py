import cv2
import numpy as np
import base64

def deep_face(img):
    # 딥러닝 기반 얼굴 인식 모델 로드
    facenet = cv2.dnn.readNet('../opencv/deploy.prototxt', '../opencv/res10_300x300_ssd_iter_140000.caffemodel')

    # 나이 추정 및 성별 추정을 위한 딥러닝 모델 로드
    age_model = cv2.dnn.readNetFromCaffe('../opencv/age_deploy.prototxt', '../opencv/age_net.caffemodel')
    gender_model = cv2.dnn.readNetFromCaffe('../opencv/gender_deploy.prototxt', '../opencv/gender_net.caffemodel')

    # 연령 및 성별 리스트 정의
    age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    gender_list = ['Male', 'Female']
    age_mid = [1, 5, 10, 17.5, 28.5, 40.5, 50.5, 80]

    # 이미지의 높이, 너비 추출
    h, w = img.shape[:2]

    # 이미지 전처리 및 얼굴 영역 검출
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=True)
    facenet.setInput(blob)
    detections = facenet.forward()

    results = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")

            # 얼굴 영역의 이미지 추출
            face_img = img[y1:y2, x1:x2]
            blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=True)

            # 검출된 얼굴 이미지를 메모리에 저장
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            _, buffer = cv2.imencode('.png', face_img)
            face_image_bytes = base64.b64encode(buffer.tobytes()).decode('utf-8')

            # 나이 추정
            age_model.setInput(blob)
            age_preds = age_model.forward()
            age = age_list[age_preds[0].argmax()]
            age_est = round(np.sum(age_mid * age_preds[0]))

            # 성별 추정
            gender_model.setInput(blob)
            gender_preds = gender_model.forward()
            gender = gender_list[gender_preds[0].argmax()]

            results.append(f"{gender}, {age_est}, {age}")

    # 이미지를 base64로 인코딩하여 반환
    _, buffer = cv2.imencode('.png', img)
    image_bytes = base64.b64encode(buffer.tobytes()).decode('utf-8')

    return results, image_bytes
