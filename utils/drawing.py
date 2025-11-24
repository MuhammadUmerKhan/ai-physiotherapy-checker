# utils/drawing.py
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_overlay(frame, results, text, color):
    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.putText(frame, text, (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 6)