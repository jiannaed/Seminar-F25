import cv2
from ultralytics import YOLO
import os
import time


VIDEO_PATH = "/Users/jd/Desktop/B2/videos/drive_sample.mov"
MODEL = "yolov8n.pt"      


DANGER_ZONE = (0.35, 0.55, 0.65, 1.0)

STOP_FILE = "/Users/jiannadong/Desktop/B2/stop_signal.txt"
print("Loading YOLO model...")
model = YOLO(MODEL)

if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Video not found: {VIDEO_PATH}")

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise IOError("❌ Could not open video.")

os.makedirs(os.path.dirname(STOP_FILE), exist_ok=True)

print("Running pedestrian STOP detection...")
print("Press 'q' to exit")

prev_time = time.time()

#reset
with open(STOP_FILE, "w") as f:
    f.write("0")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video finished.")
        break

    h, w, _ = frame.shape

    #Convert
    dz_x1 = int(DANGER_ZONE[0] * w)
    dz_y1 = int(DANGER_ZONE[1] * h)
    dz_x2 = int(DANGER_ZONE[2] * w)
    dz_y2 = int(DANGER_ZONE[3] * h)

    #Danger zone
    cv2.rectangle(frame, (dz_x1, dz_y1), (dz_x2, dz_y2), (255, 0, 0), 2)

    results = model(frame, verbose=False)

    stop_flag = False

    for box in results[0].boxes:
        cls = int(box.cls[0])
        if cls != 0:  
            continue

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

        #Person box 
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                      (0, 255, 0), 2)

        person_center_x = (x1 + x2) / 2
        person_center_y = (y1 + y2) / 2

        if (dz_x1 < person_center_x < dz_x2) and (dz_y1 < person_center_y < dz_y2):
            stop_flag = True
#stop
    if stop_flag:
        cv2.putText(frame, "STOP!", (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

        with open(STOP_FILE, "w") as f:
            f.write("1")     # simulator will read this
    else:
        with open(STOP_FILE, "w") as f:
            f.write("0")

   #FPS
    now = time.time()
    fps = 1 / (now - prev_time)
    prev_time = now

    cv2.putText(frame, f"FPS: {fps:.2f}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Pedestrian STOP System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
