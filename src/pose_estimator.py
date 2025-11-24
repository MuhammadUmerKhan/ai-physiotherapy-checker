# pose_estimator.py
import cv2
import mediapipe as mp
import numpy as np

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.last_user_results = None

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def get_symmetric_arm_angles(self, landmarks):
        lm = landmarks

        # Left arm
        l_shoulder = [lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x, lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y]
        l_elbow    = [lm[self.mp_pose.PoseLandmark.LEFT_ELBOW].x,    lm[self.mp_pose.PoseLandmark.LEFT_ELBOW].y]
        l_wrist    = [lm[self.mp_pose.PoseLandmark.LEFT_WRIST].x,    lm[self.mp_pose.PoseLandmark.LEFT_WRIST].y]
        l_hip      = [lm[self.mp_pose.PoseLandmark.LEFT_HIP].x,      lm[self.mp_pose.PoseLandmark.LEFT_HIP].y]

        # Right arm (mirrored logic)
        r_shoulder = [lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x, lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
        r_elbow    = [lm[self.mp_pose.PoseLandmark.RIGHT_ELBOW].x,    lm[self.mp_pose.PoseLandmark.RIGHT_ELBOW].y]
        r_wrist    = [lm[self.mp_pose.PoseLandmark.RIGHT_WRIST].x,    lm[self.mp_pose.PoseLandmark.RIGHT_WRIST].y]
        r_hip      = [lm[self.mp_pose.PoseLandmark.RIGHT_HIP].x,      lm[self.mp_pose.PoseLandmark.RIGHT_HIP].y]

        left_elbow_angle   = self.calculate_angle(l_shoulder, l_elbow, l_wrist)
        left_shoulder_ang  = self.calculate_angle(l_elbow, l_shoulder, l_hip)
        right_elbow_angle  = self.calculate_angle(r_shoulder, r_elbow, r_wrist)
        right_shoulder_ang = self.calculate_angle(r_elbow, r_shoulder, r_hip)

        avg_elbow = (left_elbow_angle + right_elbow_angle) / 2
        avg_shoulder = (left_shoulder_ang + right_shoulder_ang) / 2

        return [avg_elbow, avg_shoulder]

    def get_arm_angles(self, frame, is_user=False):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if results.pose_landmarks and is_user:
            self.last_user_results = results

        if results.pose_landmarks:
            return self.get_symmetric_arm_angles(results.pose_landmarks.landmark)
        return None