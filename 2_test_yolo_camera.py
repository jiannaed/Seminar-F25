import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

#builtin webcam
def get_builtin_camera(max_index=4):
    for i in range(max_index + 1):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Using camera index {i}")
                return cap
            cap.release()
    print("No webcam found")
    return None

cap = get_builtin_camera()
if cap is None:
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    #YOLO detection
    results = model(frame)
    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Pedestrian Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
