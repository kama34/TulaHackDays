from ultralytics import YOLO
import csv
from datetime import datetime

# Load a model
models = [
    "yolov8n-trained.pt",
    "yolov8s-trained.pt",
    "yolov9c-trained.pt",
    "yolov10n-trained.pt",
    "yolo11n-trained.pt",
]

# Define field names for CSV
fieldnames = ['Model', 'mAP', 'Precision', 'Recall']

# Create a unique file name based on the current date and time
csv_filename = f"valid results/results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Open the CSV file and write headers
with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each model
    for model_name in models:
        # Load and evaluate the model
        model = YOLO(model_name)
        metrics = model.val(data="/home/zemfinder/datasets/data.yaml")
        
        # Extract metrics
        map_value = metrics.box.map
        precision = metrics.box.p
        recall = metrics.box.r

        # Print the metrics to the console
        print(f"Model: {model_name}")
        print(f"mAP = {map_value}")
        print(f"Precision = {precision}")
        print(f"Recall = {recall}")
        
        # Write metrics to CSV
        writer.writerow({
            'Model': model_name,
            'mAP': map_value,
            'Precision': precision,
            'Recall': recall
        })

print(f"Results saved to {csv_filename}")
