
# Finger Mouse – Control Your Cursor with Hand Gestures

Finger Mouse is an AI-powered hand-tracking system that lets you control your computer mouse using only hand gestures. It uses computer vision to detect finger movements and translates them into cursor actions like moving, clicking, dragging, and scrolling.

## Features
- **Move Cursor** – Control the mouse with your **index finger**.
- **Click & Double-Click** – Tap your **thumb and index finger** together.
- **Drag & Drop** – Pinch your **index and middle fingers**.
- **Scrolling** – Move your **middle finger and wrist** up or down.
- **Smooth Cursor Movement** – Uses filtering to avoid sudden jumps.

## Demo
🚀 Coming soon!

## Technologies Used
- **OpenCV** – Captures and processes live video.
- **MediaPipe** – Detects and tracks hand landmarks.
- **PyAutoGUI** – Simulates mouse movements and actions.
- **NumPy & Math** – Used for coordinate mapping and distance calculations.

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/thepiratekumarno/FingerMouse.git
   cd FingerMouse
   ```
2. Install the required dependencies:
   ```sh
   pip install opencv-python mediapipe pyautogui numpy
   ```
3. Run the script:
   ```sh
   python finger_mouse.py
   ```

## How It Works
1. The webcam captures the user's hand.
2. **MediaPipe** detects hand landmarks and tracks finger positions.
3. Finger movements are mapped to screen coordinates.
4. **PyAutoGUI** moves the cursor, clicks, drags, or scrolls based on finger gestures.

## Usage
- **Move the cursor:** Hover your **index finger** in front of the camera.
- **Click:** Tap your **thumb and index finger** together.
- **Double-click:** Tap twice quickly.
- **Drag:** Pinch your **index and middle fingers** together and move.
- **Scroll:** Move your **middle finger and wrist** up or down.

## Future Improvements
- Add right-click support.
- Enhance gesture recognition for more actions.
- Optimize for lower-latency response.

## License
This project is open-source under the **MIT License**.

## Author
[Harsh Maurya](https://github.com/thepiratekumarno)
