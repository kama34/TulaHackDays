import pytesseract
from PIL import Image

# Укажите путь к изображению
img = "car_image.png"  # Замените на путь к вашему изображению

# Извлечение текста с помощью Tesseract
text = pytesseract.image_to_string(Image.open(img))

# Вывод результата
print(text)
