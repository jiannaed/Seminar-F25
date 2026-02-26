import json
import os
from PIL import Image

#paths
img_base = "/Users/jd/Desktop/B2/CityPersons/leftImg8bit/val"
ann_base = "/Users/jd/Desktop/B2/CityPersons/gtFine/val"
yolo_base = "/Users/jd/Desktop/B2/CityPersons/yolo_labels/val"
os.makedirs(yolo_base, exist_ok=True)

#YOLO format conversion
def convert_bbox(bbox, img_w, img_h):
    x_min, y_min, x_max, y_max = bbox
    x_center = ((x_min + x_max) / 2) / img_w
    y_center = ((y_min + y_max) / 2) / img_h
    w = (x_max - x_min) / img_w
    h = (y_max - y_min) / img_h
    return x_center, y_center, w, h

def bbox_from_polygon(polygon):
    xs = [pt[0] for pt in polygon]
    ys = [pt[1] for pt in polygon]
    return [min(xs), min(ys), max(xs), max(ys)]

json_files = []
for root, dirs, files in os.walk(ann_base):
    for file in files:
        if file.endswith("_polygons.json"):
            json_files.append(os.path.join(root, file))

print(f"Found {len(json_files)} annotation files.")

for json_path in json_files:
    file = os.path.basename(json_path)
    print("Processing:", file)

    with open(json_path) as f:
        data = json.load(f)

    subfolder = os.path.basename(os.path.dirname(json_path))
    img_file_candidate = file.replace("_gtFine_polygons.json", "_leftImg8bit.png")
    img_path = os.path.join(img_base, subfolder, img_file_candidate)

    if not os.path.exists(img_path):
        img_file_candidate = file.replace("_polygons.json", "_leftImg8bit.png")
        img_path = os.path.join(img_base, subfolder, img_file_candidate)

    if not os.path.exists(img_path):
        print("Missing image for:", file)
        continue

    img_w, img_h = Image.open(img_path).size
    yolo_lines = []

    for obj in data.get('objects', []):
        if obj['label'] not in ["person", "rider"]:
            continue

        if 'bbox' in obj:
            bbox = obj['bbox']
        elif 'polygon' in obj:
            bbox = bbox_from_polygon(obj['polygon'])
        else:
            continue 

        x_c, y_c, w, h = convert_bbox(bbox, img_w, img_h)
        yolo_lines.append(f"0 {x_c} {y_c} {w} {h}\n")

    if len(yolo_lines) == 0:
        print("No pedestrians found in:", file)
        continue

    txt_file = os.path.join(yolo_base, img_file_candidate.replace(".png", ".txt"))
    with open(txt_file, "w") as f:
        f.writelines(yolo_lines)

    print("Saved YOLO label:", txt_file)
