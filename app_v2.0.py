import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
import io
import os
from datetime import datetime

# Убедитесь, что путь к Tesseract указан правильно
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Описание функциональности демо
st.markdown("""
# OCR Demo: Распознавание текста на автомобильных номерах
Загрузите изображения с автомобильными номерами или выберите примеры ниже.
""")

# Настройки сессии
if "date" not in st.session_state:
    st.session_state.date = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"./input_images/{st.session_state.date}", exist_ok=True)

# Загрузка Haar Cascade
carplate_haar_cascade = cv2.CascadeClassifier('./haar_cascades/haarcascade_russian_plate_number.xml')

# Функция для детекции автомобильных номеров
def carplate_detect(image):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    for x, y, w, h in carplate_rects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
    return image, carplate_rects

# Функция для извлечения автомобильного номера
def carplate_extract(image, rects):
    for x, y, w, h in rects:
        carplate_img = image[y+15:y+h-10, x+15:x+w-20]
        return carplate_img
    return None

# Функция для увеличения изображения
def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image

# Функция для выполнения OCR
def perform_ocr(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.medianBlur(image_gray, 3)
    text = pytesseract.image_to_string(image_blur, config='--psm 6')
    return text

# Блок загрузки изображений
uploaded_files = st.file_uploader("Загрузите изображения", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
uploaded_images = []

for uploaded_file in uploaded_files:
    bytes_image = uploaded_file.read()
    name_image = uploaded_file.name
    image = Image.open(io.BytesIO(bytes_image))
    save_path = f"./input_images/{st.session_state.date}/{name_image}"
    image.save(save_path)
    uploaded_images.append(save_path)

# Функция для обработки изображений
def predict():
    with st.spinner('Обработка...'):
        results = []

        for image_path in uploaded_images:
            # Загрузка изображения
            image = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Детекция автомобильных номеров
            detected_image, carplate_rects = carplate_detect(image_rgb)
            if len(carplate_rects) > 0:
                # Извлечение номера
                carplate_img = carplate_extract(image, carplate_rects)
                if carplate_img is not None:
                    carplate_img_resized = enlarge_img(carplate_img, 150)
                    text = perform_ocr(carplate_img_resized)
                else:
                    text = "Номер не найден."
            else:
                text = "Номер не найден."

            # Сохранение результата
            results.append({"image": detected_image, "text": text})

        # Отображение результатов
        for result in results:
            st.image(result["image"], caption="Детектированное изображение", use_column_width="always")
            st.markdown(f"**Распознанный текст:**\n```\n{result['text']}\n```")

# Кнопка для запуска обработки
if st.button("Распознать текст"):
    predict()
