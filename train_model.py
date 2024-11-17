from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model.train(data="/home/zemfinder/datasets/data.yaml", epochs=200, imgsz=640)

model.save("yolo11n-trained.pt")