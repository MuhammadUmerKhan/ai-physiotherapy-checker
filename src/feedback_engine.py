# feedback_engine.py
import numpy as np

class FeedbackEngine:
    def __init__(self, tolerance=30):
        self.tolerance = tolerance

    def evaluate(self, user_angles, ref_angles):
        if user_angles is None or ref_angles is None:
            return "Detecting pose...", (255, 255, 255)

        error = np.max(np.abs(np.array(user_angles) - np.array(ref_angles)))

        if error < self.tolerance:
            return "CORRECT! PERFECT!", (0, 255, 0)
        elif error < self.tolerance + 20:
            return f"Almost there!", (0, 255, 255)
        else:
            return f"Follow along!", (0, 0, 255)