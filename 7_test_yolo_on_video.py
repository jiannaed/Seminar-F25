import cv2
from ultralytics import YOLO
import time
import os

VIDEO_PATH = "/Users/jd/Desktop/B2/videos/drive_sample.mov"
MODEL_WEIGHTS = "yolov8n.pt"

model = YOLO(MODEL_WEIGHTS)
if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Video file not found: {VIDEO_PATH}")

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise IOError("Failed to open the video file.")

print("Video loaded successfully!")
print("Press 'q' to quit.")


prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video ended.")
        break

    #yolo prediction
    results = model(frame, verbose=False)
    annotated = results[0].plot()

    #FPS calculation
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    #FPS display 
    cv2.putText(annotated, f"FPS: {fps:.2f}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("YOLO Driving Scene Detection", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

