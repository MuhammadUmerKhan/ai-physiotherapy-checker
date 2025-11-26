# video_handler.py
import cv2
import os
from src.config import REFERENCE_VIDEO, FRAME_WIDTH, FRAME_HEIGHT

class VideoHandler:
    def __init__(self):
        if not os.path.exists(REFERENCE_VIDEO):
            raise FileNotFoundError(f"Reference video not found: {REFERENCE_VIDEO}")

        self.ref_cap = cv2.VideoCapture(REFERENCE_VIDEO)
        self.cam = cv2.VideoCapture(0)

        if not self.cam.isOpened():
            raise ConnectionError("Cannot open webcam")

    def get_reference_frame(self):
        ret, frame = self.ref_cap.read()
        if not ret:
            self.ref_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.ref_cap.read()
        if ret:
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            return frame
        return None

    def get_user_frame(self):
        ret, frame = self.cam.read()
        if ret:
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            return frame
        return None

    def release(self):
        self.ref_cap.release()
        self.cam.release()