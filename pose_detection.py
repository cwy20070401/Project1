import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

colorDots = mp_drawing.DrawingSpec(color=(80,110,10), thickness=3, circle_radius=1)
colorConnects = mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=3, circle_radius=1)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while True:
        _, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = holistic.process(imgRGB)

        mp_drawing.draw_landmarks(img, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,landmark_drawing_spec=(colorDots), connection_drawing_spec=(colorConnects))

        # print(results.pose_landmarks.landmark[11])

        if results.pose_landmarks:
            if(results.pose_landmarks.landmark[11].visibility > 0.5):
                height, width, channel = img.shape
                cx, cy = int(results.pose_landmarks.landmark[11].x * width), int(results.pose_landmarks.landmark[11].y * height)
                cv2.circle(img, (cx, cy), 10, (125, 0, 125), 3)

        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        cv2.imshow('img', img)
        if cv2.waitKey(1) == 27:
            break