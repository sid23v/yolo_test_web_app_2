import cv2
from ultralytics import YOLO
import threading

class VideoCamera:
    def __init__(self):
        self.model = YOLO("models/best_4.pt")  
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.is_running = False
        self.lock = threading.Lock()

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False
        self.cap.release()

    def get_frame(self):
        if not self.is_running:
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        # Run YOLO inference
        results = self.model(frame, conf=0.5, verbose=False)
        annotated_frame = results[0].plot()

        # Encode as JPEG
        ret, jpeg = cv2.imencode('.jpg', annotated_frame)
        return jpeg.tobytes()
