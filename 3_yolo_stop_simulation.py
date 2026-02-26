import cv2
import numpy as np
from ultralytics import YOLO
import glob
import os

model = YOLO("yolov8n.pt")  # pretrained on COCO

image_folder = "/Users/jd/Desktop/B2/coco_sample/"
os.makedirs(image_folder, exist_ok=True)
sample_urls = [
    "https://ultralytics.com/images/zidane.jpg",
    "https://ultralytics.com/images/bus.jpg"]

for url in sample_urls:
    filename = os.path.join(image_folder, url.split("/")[-1])
    if not os.path.exists(filename):
        import urllib.request
        urllib.request.urlretrieve(url, filename)
image_paths = sorted(glob.glob(image_folder + "*.jpg"))

def get_roi(frame):
    h, w, _ = frame.shape
    roi = np.array([
        [int(0.3*w), int(0.6*h)],
        [int(0.7*w), int(0.6*h)],
        [int(0.9*w), h],
        [int(0.1*w), h]
    ])
    return roi

def point_in_polygon(point, polygon):
    return cv2.pointPolygonTest(polygon, point, False) >= 0

print("Press 'q' to quit")

for img_path in image_paths:
    frame = cv2.imread(img_path)
    if frame is None:
        continue

    roi = get_roi(frame)
    results = model(frame)

    annotated_frame = frame.copy()
    cv2.polylines(annotated_frame, [roi], isClosed=True, color=(0,255,0), thickness=2)
    stop_triggered = False

    #detections
    for box in results[0].boxes:
        cls = int(box.cls[0])
        if cls != 0:  # only person
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255,0,0), 2)

        bx = int((x1 + x2)/2)
        by = int(y2)
        cv2.circle(annotated_frame, (bx, by), 5, (0,0,255), -1)

        if point_in_polygon((bx, by), roi):
            stop_triggered = True

    if stop_triggered:
        cv2.putText(annotated_frame, "STOP!", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

    cv2.imshow("YOLO Pedestrian STOP Simulation", annotated_frame)
    key = cv2.waitKey(0)  
    if key & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
