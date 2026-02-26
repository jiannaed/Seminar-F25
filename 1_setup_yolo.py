from ultralytics import YOLO

model = YOLO("yolov8n.pt")

print(model.info())
print("YOLO model loaded successfully.")