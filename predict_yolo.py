import cv2
from PIL import Image
from ultralytics import YOLO

model = YOLO("yolo11n.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
# results = model.predict(source="satelite.jpeg")
results = model.predict(source="satellite", save=True, show=False)
print(f"Result: {results}")

#from PIL
# im1 = Image.open("satelite.jpeg")
# results = model.predict(source=im1, save=True) # save plotted images

# from ndarray
# im2 = cv2.imread("satelite.jpeg")
# results = model.predict(source=im2, save=True, save_txt=True) # save prediction as labels

# from list of PIL/ndarray
# results = model.predict(source=[im1, im2])