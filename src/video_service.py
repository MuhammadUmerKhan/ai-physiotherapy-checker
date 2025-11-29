# video_service.py
import cv2
from config import REFERENCE_VIDEOS_FOLDER, FRAME_WIDTH, FRAME_HEIGHT

class VideoService:
    def __init__(self, video_name: str):
        path = f"{REFERENCE_VIDEOS_FOLDER}/{video_name}"
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open reference video: {video_name}")
        self.frame_count = 0

    def get_next_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            return frame
        return None

    def release(self):
        self.cap.release()