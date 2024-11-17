from PIL import Image
from ultralytics import YOLO

class Model:
    def __init__(self, model_name):
        match model_name:
            case "YOLOv8n":
                self.name = "yolov8n.pt"
            case "YOLOv8n-Trained":
                self.name = "yolov8n-trained.pt"
            case "YOLOv8s":
                self.name = "yolov8s.pt"
            case "YOLOv8s-Trained":
                self.name = "yolov8s-trained.pt"
            case "YOLOv9c":
                self.name = "yolov9c.pt"
            case "YOLOv9c-Trained":
                self.name = "yolov9c-trained.pt"
            case "YOLOv10n":
                self.name = "yolov10n.pt"
            case "YOLOv10n-Trained":
                self.name = "yolov10n-trained.pt"
            case "YOLOv11n":
                self.name = "yolo11n.pt"
            case "YOLOv11n-Trained":
                self.name = "yolo11n-trained.pt"
            case _:
                self.name = "Model"
        self.model = YOLO(self.name)
    
    def predict(self, image_path):
        return self.model.predict(source=image_path, save=True, show_labels=False, conf=0.6)