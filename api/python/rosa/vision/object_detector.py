from collections import namedtuple
from ultralytics import YOLO
import os
import cv2

VisualObject = namedtuple('VisualObject',
                          ('label', 'center', 'box', 'confidence'))



class YoloDetector:
    _model = None  # Class attribute to hold the model

    def __init__(self):
        # Initialize the model only once
        if YoloDetector._model is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, 'best.pt')
            YoloDetector._model = YOLO(model_path)

    def detect_objects(self, img, threshold=0.2):
        if img is None:
            return []

        results = YoloDetector._model(img)[0]  # Use the class-level model
        found_objs = []

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > threshold:
                label = results.names[int(class_id)]
                center = ((x1 + x2) / 2, (y1 + y2) / 2)
                box = (x1, y1, x2, y2)
                obj = VisualObject(label, center, box, score)
                found_objs.append(obj)

        return found_objs

color_dict = {
    "cube" : (0, 255, 0),
    "triangle" : (255, 0, 0),
    "star" : (0, 0, 255),
}

def detect_objects(img, render=False):
    results = YoloDetector().detect_objects(img)
    
    if render:
        for obj in results:
            x1, y1, x2, y2 = obj.box
            label = obj.label
            score = obj.confidence
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color_dict[label], 2)
            cv2.putText(img, f"{label} ({score:.2f})", (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_dict[label], 2)
            
    return results
