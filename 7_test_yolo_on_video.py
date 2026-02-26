import cv2
from ultralytics import YOLO
import time
import os

# ---------------------------
# CONFIGURATION
# ---------------------------
VIDEO_PATH = "/Users/jiannadong/Desktop/B2/videos/drive_sample.mov"
MODEL_WEIGHTS = "yolov8n.pt"   # you can replace with cityscapes weights later

# ---------------------------
# LOAD MODEL
# ---------------------------
print("Loading YOLO model...")
model = YOLO(MODEL_WEIGHTS)

# ---------------------------
# LOAD VIDEO
# ---------------------------
if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Video file not found: {VIDEO_PATH}")

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise IOError("❌ Failed to open the video file.")

print("Video loaded successfully!")
print("Press 'q' to quit.")

# ---------------------------
# PROCESS VIDEO FRAME-BY-FRAME
# ---------------------------
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video ended.")
        break

    # YOLO prediction
    results = model(frame, verbose=False)

    # Render bounding boxes
    annotated = results[0].plot()

    # FPS Calculation
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Display FPS on frame
    cv2.putText(annotated, f"FPS: {fps:.2f}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show window
    cv2.imshow("YOLO Driving Scene Detection", annotated)

    # Quit if q pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

