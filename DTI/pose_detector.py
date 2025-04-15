import cv2
import mediapipe as mp
import numpy as np
import time
import os

# Global score
current_score = 0

# Define and export absolute path to trigger file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRIGGER_PATH = os.path.join(BASE_DIR, "static", "trigger_result.txt")
os.makedirs(os.path.join(BASE_DIR, "static"), exist_ok=True)
if not os.path.exists(TRIGGER_PATH):
    with open(TRIGGER_PATH, "w") as f:
        f.write("")

# MediaPipe pose setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

def classify_pose(landmarks):
    ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    le = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    lw = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    re = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    rw = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    lk = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
    la = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    rk = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
    ra = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    laa = calculate_angle(ls, le, lw)
    raa = calculate_angle(rs, re, rw)
    lla = calculate_angle(lh, lk, la)
    rla = calculate_angle(rh, rk, ra)

    if 160 < laa < 190 and 160 < raa < 190 and 160 < lla < 190 and 160 < rla < 190:
        return "Mountain Pose"
    return "Unknown"

def generate_frames():
    global current_score

    # Reset the trigger result file at the start
    with open(TRIGGER_PATH, "w") as f:
        f.write("")

    cap = cv2.VideoCapture(0)
    target_pose = "Mountain Pose"
    pose_hold_frames = 0
    required_frames = 30

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            label = "No pose"
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                landmarks = results.pose_landmarks.landmark
                label = classify_pose(landmarks)

            cv2.putText(image, f'Target: {target_pose}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(image, f'Pose: {label}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if label == target_pose:
                pose_hold_frames += 1
                cv2.putText(image, 'Hold Pose to Win!', (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                pose_hold_frames = 0

            if pose_hold_frames >= required_frames:
                current_score = 1
                cap.release()
                with open(TRIGGER_PATH, "w") as f:
                    f.write("done")
                break

            ret, buffer = cv2.imencode('.jpg', image)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()

def get_score():
    global current_score
    return current_score
