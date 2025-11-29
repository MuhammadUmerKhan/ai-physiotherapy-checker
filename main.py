# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
from src.pose_processor import PoseProcessor
from src.video_service import VideoService
from schemas.schemas import FeedbackResponse
import cv2
import numpy as np
import base64
import asyncio

app = FastAPI(title="Real-Time Exercise Coach API")

# Global reference video service (can be changed per user later)
current_video_service = VideoService("usama.mp4")
pose_processor = PoseProcessor()

def frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    return base64.b64encode(buffer).decode('utf-8')

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1>Exercise Coach API is Running</h1>
    <p>Use WebSocket at: <code>ws://localhost:8000/ws/coach/{video_name}</code></p>
    <p>Send webcam frames as binary JPEG → Receive feedback + coach frame</p>
    """

@app.websocket("/ws/coach/{video_name}")
async def websocket_endpoint(websocket: WebSocket, video_name: str):
    await websocket.accept()
    global current_video_service
    try:
        # Restart video service with new video
        current_video_service.release()
        current_video_service = VideoService(video_name)

        while True:
            # Receive user webcam frame (binary)
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            user_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if user_frame is None:
                await websocket.send_json({"error": "Invalid frame"})
                continue

            user_frame = cv2.resize(user_frame, (640, 480))

            # Get current coach frame
            coach_frame = current_video_service.get_next_frame()
            if coach_frame is None:
                coach_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(coach_frame, "Video Error", (100, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

            # Process both frames
            user_rgb = cv2.cvtColor(user_frame, cv2.COLOR_BGR2RGB)
            coach_rgb = cv2.cvtColor(coach_frame, cv2.COLOR_BGR2RGB)

            user_results = pose_processor.pose.process(user_rgb)
            coach_results = pose_processor.pose.process(coach_rgb)

            # Draw skeleton on user
            if user_results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    user_frame, user_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Compare and get feedback
            feedback, error, is_correct = pose_processor.compare_poses(
                coach_results.pose_landmarks, user_results.pose_landmarks)

            # Add text
            cv2.putText(coach_frame, "COACH", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 5)
            cv2.putText(user_frame, "YOU", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5)
            color = (0, 255, 0) if is_correct else (0, 0, 255)
            cv2.putText(user_frame, feedback, (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.8, color, 5)

            # Encode both frames
            coach_b64 = frame_to_base64(coach_frame)
            user_b64 = frame_to_base64(user_frame)

            # Send back to frontend
            await websocket.send_json({
                "coach_frame": f"data:image/jpeg;base64,{coach_b64}",
                "user_frame": f"data:image/jpeg;base64,{user_b64}",
                "feedback": feedback,
                "error": error,
                "is_correct": is_correct
            })

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        current_video_service.release()