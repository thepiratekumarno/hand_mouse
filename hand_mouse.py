import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

class AdvancedFingerMouse:
    def __init__(self):
        # Hand tracking setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.cap = cv2.VideoCapture(0)
        
        # Screen properties
        self.screen_w, self.screen_h = pyautogui.size()
        
        # Control parameters
        self.smoothing = 5
        self.ploc_x, self.ploc_y = 0, 0
        self.cloc_x, self.cloc_y = 0, 0
        self.frame_reduction = 100
        self.click_thresh = 30
        self.drag_thresh = 40
        self.scroll_thresh = 50
        self.zoom_thresh = 50
        
        # State tracking
        self.dragging = False
        self.scrolling = False
        self.last_click = 0

    def get_hand_position(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        landmarks = []
        
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(hand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append((id, cx, cy))
        return landmarks

    def process_gestures(self, landmarks, img):
        if not landmarks:
            return

        # Get key points
        index_tip = landmarks[8][1:]
        middle_tip = landmarks[12][1:]
        thumb_tip = landmarks[4][1:]
        wrist = landmarks[0][1:]

        # Cursor control with index finger
        x = np.interp(index_tip[0], 
                     (self.frame_reduction, self.cap.get(3)-self.frame_reduction),
                     (0, self.screen_w))
        y = np.interp(index_tip[1],
                     (self.frame_reduction, self.cap.get(4)-self.frame_reduction),
                     (0, self.screen_h))
        
        # Smooth cursor movement
        self.cloc_x = self.ploc_x + (x - self.ploc_x) / self.smoothing
        self.cloc_y = self.ploc_y + (y - self.ploc_y) / self.smoothing
        
        pyautogui.moveTo(self.screen_w - self.cloc_x, self.cloc_y)
        self.ploc_x, self.ploc_y = self.cloc_x, self.cloc_y

        # Click detection (index and thumb)
        click_dist = math.hypot(index_tip[0]-thumb_tip[0], index_tip[1]-thumb_tip[1])
        
        # Drag detection (index and middle finger)
        drag_dist = math.hypot(index_tip[0]-middle_tip[0], index_tip[1]-middle_tip[1])
        
        # Scroll detection (middle finger and wrist)
        scroll_dist = math.hypot(middle_tip[0]-wrist[0], middle_tip[1]-wrist[1])
        
        # Zoom detection (index finger and thumb distance)
        zoom_dist = math.hypot(index_tip[0]-thumb_tip[0], index_tip[1]-thumb_tip[1])
        
        # Action handling
        if click_dist < self.click_thresh:
            if time.time() - self.last_click < 0.3:
                pyautogui.doubleClick()
            else:
                pyautogui.click()
            self.last_click = time.time()

        elif drag_dist < self.drag_thresh:
            if not self.dragging:
                pyautogui.mouseDown()
                self.dragging = True
        else:
            if self.dragging:
                pyautogui.mouseUp()
                self.dragging = False

        if scroll_dist < self.scroll_thresh:
            scroll_amount = (wrist[1] - middle_tip[1]) / 10
            pyautogui.scroll(int(scroll_amount))
        
        if zoom_dist < self.zoom_thresh:
            pyautogui.hotkey('ctrl', '+')  # Zoom in
        elif zoom_dist > self.zoom_thresh + 20:
            pyautogui.hotkey('ctrl', '-')  # Zoom out

        # Visual feedback
        cv2.circle(img, (index_tip[0], index_tip[1]), 15, (0,255,0), cv2.FILLED)
        cv2.putText(img, "Finger Mouse Active", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    
    def run(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)
            
            landmarks = self.get_hand_position(img)
            self.process_gestures(landmarks, img)
            
            cv2.imshow("Advanced Finger Mouse", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    fm = AdvancedFingerMouse()
    fm.run()
