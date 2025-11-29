# pose_processor.py
import cv2
import mediapipe as mp
import numpy as np
from config import TOLERANCE

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class PoseProcessor:
    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def get_arm_angles(self, landmarks):
        lm = landmarks.landmark

        # Extract points
        l_shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
        l_elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW].y]
        l_wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST].x, lm[mp_pose.PoseLandmark.LEFT_WRIST].y]
        l_hip = [lm[mp_pose.PoseLandmark.LEFT_HIP].x, lm[mp_pose.PoseLandmark.LEFT_HIP].y]

        r_shoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
        r_elbow = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW].x, lm[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
        r_wrist = [lm[mp_pose.PoseLandmark.RIGHT_WRIST].x, lm[mp_pose.PoseLandmark.RIGHT_WRIST].y]
        r_hip = [lm[mp_pose.PoseLandmark.RIGHT_HIP].x, lm[mp_pose.PoseLandmark.RIGHT_HIP].y]

        left_elbow = self.calculate_angle(l_shoulder, l_elbow, l_wrist)
        left_shoulder = self.calculate_angle(l_elbow, l_shoulder, l_hip)
        right_elbow = self.calculate_angle(r_shoulder, r_elbow, r_wrist)
        right_shoulder = self.calculate_angle(r_elbow, r_shoulder, r_hip)

        avg_elbow = (left_elbow + right_elbow) / 2
        avg_shoulder = (left_shoulder + right_shoulder) / 2

        return np.array([avg_elbow, avg_shoulder])

    def compare_poses(self, ref_landmarks, user_landmarks):
        if not ref_landmarks or not user_landmarks:
            return "Detecting pose...", 999, False

        ref_angles = self.get_arm_angles(ref_landmarks)
        user_angles = self.get_arm_angles(user_landmarks)

        error = np.max(np.abs(user_angles - ref_angles))

        if error < TOLERANCE:
            return "CORRECT! PERFECT!", round(error, 1), True
        elif error < TOLERANCE + 20:
            return f"Almost there!", round(error, 1), False
        else:
            return f"Follow the coach!", round(error, 1), False