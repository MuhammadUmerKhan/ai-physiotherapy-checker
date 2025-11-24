# main.py
from video_handler import VideoHandler
from pose_estimator import PoseEstimator
from feedback_engine import FeedbackEngine
from utils.drawing import draw_overlay
import cv2

def main():
    handler = VideoHandler()
    estimator = PoseEstimator()
    feedback_engine = FeedbackEngine(tolerance=38)

    print("\n" + "="*60)
    print("   REAL-TIME EXERCISE COACH STARTED!")
    print("   Follow the coach on the left → Get green 'CORRECT!'")
    print("   Press 'q' to quit")
    print("="*60 + "\n")

    while True:
        ref_frame = handler.get_reference_frame()
        user_frame = handler.get_user_frame()

        if ref_frame is None or user_frame is None:
            break

        # Process poses
        ref_angles = estimator.get_arm_angles(ref_frame)
        user_angles = estimator.get_arm_angles(user_frame, is_user=True)

        # Get feedback
        feedback, color = feedback_engine.evaluate(user_angles, ref_angles)

        # Draw skeletons and feedback
        if estimator.last_user_results:
            draw_overlay(user_frame, estimator.last_user_results, feedback, color)

        # Labels
        cv2.putText(ref_frame, "COACH", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 5)
        cv2.putText(user_frame, "YOU", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 5)

        # Combine and show
        combined = cv2.hconcat([ref_frame, user_frame])
        cv2.imshow("Real-Time Exercise Coach - Follow the Coach!", combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    handler.release()
    cv2.destroyAllWindows()
    print("Workout finished! Great job!")

if __name__ == "__main__":
    main()