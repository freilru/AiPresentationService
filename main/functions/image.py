import json
import time
import requests
from PIL import Image
from io import BytesIO
import base64
import os
from django.conf import settings

# Класс для работы с API генерации изображений
class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    # Получение доступной модели
    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    # Запуск генерации изображения
    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    # Проверка статуса генерации
    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    # Сохранение сгенерированного изображения
    def save_image(self, image_data, save_path):
        if image_data.startswith('/9j/'):
            image_data = 'data:image/jpeg;base64,' + image_data

        base64_str = image_data.split('base64,')[1]
        img = Image.open(BytesIO(base64.b64decode(base64_str)))

        img.save(save_path)


# Основная функция генерации изображения
def gen(prompt, format=2):
    format = int(format)
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'CDCE3F9E573C26F42865C12A0FBB3D69',
                        '69AF86776DFE0A6547329898D053F7EE')

    # Получение модели
    model_id = api.get_model()

    # Определение размеров изображения
    width, height = 1024, 1024
    if format == 1:
        width, height = 1024, 1024
    elif format == 2:
        width, height = 1920, 1080
    elif format == 3:
        width, height = 1080, 1920

    print(width, height)

    # Запуск генерации
    uuid = api.generate(prompt, model_id, width=width, height=height)

    # Получение результата
    images = api.check_generation(uuid)

    # Генерация уникального имени файла
    unique_filename = f"generated_image_{uuid}.png"

    # Определение пути для сохранения
    media_path = os.path.join(settings.MEDIA_ROOT, 'generated_images')
    os.makedirs(media_path, exist_ok=True)
    full_path = os.path.join(media_path, unique_filename)

    # Сохранение изображения
    api.save_image(images[0], full_path)

    # Формирование URL для доступа к изображению
    image_url = f"{settings.MEDIA_URL}generated_images/{unique_filename}"

    return image_url