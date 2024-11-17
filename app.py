import streamlit as st
from PIL import Image
import io
import os
from os import walk
from datetime import datetime
import requests

from roboflow import Roboflow

# Описание функциональности демо
st.markdown("""
# Это демо сайт, который продемонстрирует работу ИИ по детекции и классификации контейнеров
У нас возможна детекция следующих вариантов:
""")

# Инициализация модели Roboflow
rf = Roboflow(api_key="d6PoPvkjGCOvvPkoMxJB")
project = rf.workspace().project("garbage-containers-ntlho")
model = project.version(1).model

# Настройки сессии
if "date" not in st.session_state:
    st.session_state.date = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"./input_images/{st.session_state.date}", exist_ok=True)

st.markdown("""
### Выберите базовые изображения или загрузите свои
""")

# Пути к базовым изображениям
path_clear = "http://152.42.239.85:8082/app/static/clear.jpg"
path_full = "http://152.42.239.85:8082/app/static/full.jpg"
path_svalka = "http://152.42.239.85:8082/app/static/svalka.jpg"

# Блок выбора базовых изображений
col1, col2, col3 = st.columns(3)

with col1:
    st.image(path_clear, caption="Clear")
    checkbox_clear = st.checkbox("Clear", key="clear")

with col2:
    st.image(path_full, caption="Full")
    checkbox_full = st.checkbox("Full", key="full")

with col3:
    st.image(path_svalka, caption="Svalka")
    checkbox_svalka = st.checkbox("Svalka", key="svalka")

# Функция для загрузки изображения с URL
def download_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Проверка успешности запроса
    return Image.open(io.BytesIO(response.content))

# Загрузка изображений
uploaded_files = st.file_uploader(
    "Загрузите изображения", accept_multiple_files=True, type=['png', 'jpg', 'jpeg']
)
uploaded_images = []

for uploaded_file in uploaded_files:
    bytes_image = uploaded_file.read()
    name_image = uploaded_file.name
    image = Image.open(io.BytesIO(bytes_image))
    save_path = f"./input_images/{st.session_state.date}/{name_image}"
    image.save(save_path)
    uploaded_images.append(save_path)

from PIL import ImageDraw, ImageFont

# Функция для отрисовки детекций
from PIL import ImageDraw

# Функция для отрисовки детекций
from PIL import ImageDraw

# Функция для отрисовки детекций
def draw_predictions(image_path, predictions):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for prediction in predictions:
        # Координаты бокса
        x = prediction['x']
        y = prediction['y']
        width = prediction['width']
        height = prediction['height']

        # Верхний левый и нижний правый угол
        top_left = (x - width / 2, y - height / 2)
        bottom_right = (x + width / 2, y + height / 2)

        # Нарисовать прямоугольник
        draw.rectangle([top_left, bottom_right], outline="red", width=3)

        # Добавить подпись (класс и вероятность)
        label = f"{prediction['class']} ({prediction['confidence']:.2f})"

        # Рассчитать размеры текста
        text_bbox = draw.textbbox((0, 0), label)  # Получаем координаты области текста
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_position = (top_left[0], top_left[1] - text_height - 5)  # Разместить текст выше прямоугольника
        background_position = [
            (text_position[0], text_position[1]),
            (text_position[0] + text_width, text_position[1] + text_height),
        ]

        # Нарисовать фон для текста
        draw.rectangle(background_position, fill="white")

        # Нарисовать текст поверх фона
        draw.text(text_position, label, fill="red")

    return image



# Функция для выполнения предсказания
def predict():
    with st.spinner('Обработка...'):
        results = []

        # Обработка базовых изображений
        if checkbox_clear:
            image = download_image_from_url(path_clear)
            image_path = f"./input_images/{st.session_state.date}/clear.jpg"
            image.save(image_path)
            prediction = model.predict(image_path).json()
            results.append({"image": image_path, "prediction": prediction})

        if checkbox_full:
            image = download_image_from_url(path_full)
            image_path = f"./input_images/{st.session_state.date}/full.jpg"
            image.save(image_path)
            prediction = model.predict(image_path).json()
            results.append({"image": image_path, "prediction": prediction})

        if checkbox_svalka:
            image = download_image_from_url(path_svalka)
            image_path = f"./input_images/{st.session_state.date}/svalka.jpg"
            image.save(image_path)
            prediction = model.predict(image_path).json()
            results.append({"image": image_path, "prediction": prediction})

        # Обработка загруженных изображений
        for image_path in uploaded_images:
            prediction = model.predict(image_path).json()
            results.append({"image": image_path, "prediction": prediction})

        # Отображение результатов
        for result in results:
            # Нарисовать детекции на изображении
            detected_image = draw_predictions(result["image"], result["prediction"]["predictions"])
            st.image(detected_image, caption="Detected Image", use_column_width="always")



# Кнопка для запуска предсказания
if st.button("Предсказать"):
    predict()
