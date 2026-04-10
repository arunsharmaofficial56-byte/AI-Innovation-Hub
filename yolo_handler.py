import cv2
from ultralytics import YOLO
import os

class YOLOHandler:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.classes = self.model.names

    def detect_image(self, image_path, output_path, conf_threshold=0.25):
        results = self.model(image_path, conf=conf_threshold)
        res = results[0]
        
        # Save processed image
        res.save(filename=output_path)
        
        detections = []
        for box in res.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            detections.append({
                "label": self.classes[cls],
                "confidence": round(conf * 100, 2),
                "bbox": xyxy
            })
            
        return detections

    def get_stream_frame(self, frame, conf_threshold=0.25):
        results = self.model(frame, conf=conf_threshold, verbose=False)
        res = results[0]
        
        # Plot boxes on the frame
        annotated_frame = res.plot()
        
        detections = []
        for box in res.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            detections.append({
                "label": self.classes[cls],
                "confidence": round(conf * 100, 2)
            })
            
        return annotated_frame, detections
