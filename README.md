# 🏋️‍♂️ AI Physiotherapy Checker - Real-Time Exercise Coach API
### Follow the coach on video → Get instant **"CORRECT!"** feedback when your form is perfect!

This project uses **FastAPI + MediaPipe + OpenCV** to compare your live posture to a coach video in real time via WebSocket.  
You get instant feedback on your form with color-coded guidance — perfect for home workouts like:

- Bicep curls  
- Shoulder press  
- Lateral raises  
- Squats  
- Push-ups  
- & more!

---

## 🚀 Features

- 🌐 **FastAPI WebSocket API**  
  - Real-time communication for instant feedback
  - Easy integration with web/mobile frontends

- 🎥 **Side-by-side view**  
  - Coach video frame  
  - Your webcam feed with skeleton overlay

- 🦴 **Real-time skeleton pose tracking**

- 🎯 **Smart color-based posture feedback**  
  - **Green:** Perfect form!  
  - **Red:** Follow the coach

- ⚙️ Adjustable angle tolerance — starts easy at **38°** (modifiable in `src/config.py`)

- 🎬 Works with **any front-facing exercise video**

---

## 📁 Folder Structure

```
ai-physiotherapy-checker/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project configuration
├── README.md
├── LICENSE
├── todo.txt
├── assets/                 # Static assets
├── schemas/
│   └── schemas.py          # Pydantic response models
├── src/
│   ├── __init__.py
│   ├── config.py           # Settings (tolerance, frame size, video folder)
│   ├── pose_processor.py   # MediaPipe pose processing & comparison
│   └── video_service.py    # Reference video handling
└── reference_videos/
    └── usama.mp4           # Put your coach videos here
```

---

## 🔧 Installation & Setup (Step by Step)

### 1️⃣ Clone or download this project

```bash
git clone https://github.com/MuhammadUmerKhan/ai-physiotherapy-checker.git
cd ai-physiotherapy-checker
```

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
```

### 3️⃣ Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4️⃣ Install required libraries

```bash
pip install -r requirements.txt
```

### 5️⃣ Add your reference video

Place your coach/reference video in the `reference_videos/` folder:
```
reference_videos/usama.mp4
```

---

## 🚀 Running the FastAPI Server

### Start the server with Uvicorn:

```bash
uvicorn main:app --reload
```

Or specify host and port:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Access the API:

- **Home Page:** http://localhost:8000
- **API Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

---

## 🔌 WebSocket API Usage

### Endpoint:
```
ws://localhost:8000/ws/coach/{video_name}
```

### How it works:
1. Connect to the WebSocket with your reference video name (e.g., `usama.mp4`)
2. Send webcam frames as **binary JPEG** data
3. Receive JSON response with:
   - `coach_frame`: Base64 encoded coach video frame
   - `user_frame`: Base64 encoded user frame with skeleton overlay
   - `feedback`: Text feedback ("CORRECT!" or "Follow Coach")
   - `error`: Numerical error value
   - `is_correct`: Boolean indicating if form is correct

### Example Response:
```json
{
  "coach_frame": "data:image/jpeg;base64,...",
  "user_frame": "data:image/jpeg;base64,...",
  "feedback": "CORRECT!",
  "error": 15.5,
  "is_correct": true
}
```

---

## ⚙️ Configuration

Edit `src/config.py` to customize:

```python
TOLERANCE = 38              # Angle tolerance in degrees
FRAME_WIDTH = 640           # Frame width
FRAME_HEIGHT = 480          # Frame height
REFERENCE_VIDEOS_FOLDER = "reference_videos"
```

---

## 📦 Dependencies

- `fastapi` - Modern web framework for APIs
- `uvicorn` - ASGI server
- `opencv-python` - Computer vision
- `mediapipe` - Pose estimation
- `numpy` - Numerical operations
- `python-multipart` - File uploads
- `Pillow` - Image processing

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal to stop the server.


