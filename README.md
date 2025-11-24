# 🏋️‍♂️ Real-Time Exercise Coach  
### Follow the coach on video → Get instant **“CORRECT!”** feedback when your form is perfect!

This project uses **MediaPipe + OpenCV** to compare your live posture to a coach video in real time.  
You get instant feedback on your form with color-coded guidance — perfect for home workouts like:

- Bicep curls  
- Shoulder press  
- Lateral raises  
- Squats  
- Push-ups  
- & more!

<img src="https://via.placeholder.com/800x400?text=Demo+Screenshot+Coming+Soon" alt="Demo" width="100%"/>

---

## 🚀 Features

- 🎥 **Side-by-side view**  
  - Coach video (left)  
  - Your webcam feed (right)

- 🦴 **Real-time skeleton pose tracking**

- 🎯 **Smart color-based posture feedback**  
  - **Green:** Perfect form!  
  - **Yellow:** Almost there  
  - **Red:** Follow the coach

- ⚙️ Adjustable angle tolerance — starts easy at **38°** (modifiable in `config.py`)

- 🎬 Works with **any front-facing exercise video**

---

## 📁 Folder Structure

exercise_coach/
├── main.py # Run this file
├── config.py # Easy settings (video path, tolerance, etc.)
├── pose_estimator.py
├── video_handler.py
├── feedback_engine.py
├── utils/
│ └── drawing.py
├── reference_videos/
│ └── usama.mp4 # Put your coach video here
├── requirements.txt
└── README.md 



---

# 🔧 Installation & Setup (Step by Step)

## 1️⃣ Clone or download this project

```bash
git clone https://github.com/muneeb502/exercise_coach.git
cd exercise_coach

## Create a virtual environment (recommended)


python -m venv venv


## Activate it:

### Windows

venv\Scripts\activate


## Install required libraries

pip install -r requirements.txt

## Add your reference video

reference_videos/usama.mp4

## Run the app!
python main.py

## Press q anytime to quit.


