# Импорты
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Slide, Presentation, Theme
from .forms import PresentationForm
from main.functions.image import gen
from main.functions.yandexapi import send_to_gen_pres, send_to_change_text, send_to_proceed_comm

import json
import os

# Основные представления
def index(request):
    """Отображение главной страницы"""
    presentation = Presentation.objects.first()  # Получаем первую презентацию
    slides = json.loads(presentation.slides) if presentation else []
    return render(request, 'index.html', {'slides': slides, 'presentation': presentation})

def edit(request, presentation_id):
    """Редактирование презентации"""
    presentation = Presentation.objects.get(id=presentation_id)
    slides = Slide.objects.all().order_by('index')
    instance = json.loads(presentation.slides)
    comments = json.loads(presentation.comments) if presentation.comments else []

    return render(request, 'index.html', {'presentation': presentation, 'slides': slides, 'instance': instance, 'comments': comments})

def create(request):
    """Создание новой презентации"""
    if request.method == 'POST':
        form = PresentationForm(request.POST)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.user = request.user
            
            # Получаем текстовый файл и переводим его в строку
            text_file = request.FILES.get('text_file')
            if text_file:
                text_content = text_file.read().decode('utf-8')
            
            # Получаем выбранную тему
            selected_theme = request.POST.get('theme')
            theme = Theme.objects.get(id=selected_theme)
            # Получаем JSON с презентацией
            presentation_json = send_to_gen_pres(text_content, theme.slides_json)
            presentation.slides = presentation_json
            presentation.save()

            # Парсим JSON
            slides_data = json.loads(presentation_json)

            # Проходим по всем слайдам и генерируем изображения
            for slide in slides_data:
                for key, value in slide['content'].items():
                    if key.startswith('img-'):
                        # Генерируем изображение
                        image_url = gen(value)
                        # Обновляем значение в JSON
                        slide['content'][key] = image_url

            # Сохраняем обновленный JSON
            presentation.slides = json.dumps(slides_data).replace('\n', '').replace('"', '\"').replace("```", '').replace('fields', 'content')
            presentation.save()
            presentation.save()
            return redirect('edit', presentation_id=presentation.id)
    else:
        form = PresentationForm()
    
    # Получаем все шаблоны и слайды для отображения в форме
    themes = Theme.objects.all()
    slides = Slide.objects.all()
    
    return render(request, 'create.html', {
        'form': form,
        'themes': themes,
        'slides': slides
    })

# Функции для работы с презентацией
@csrf_exempt
def save_presentation(request, presentation_id):
    """Сохранение презентации"""
    if request.method == 'POST':
        presentation = Presentation.objects.get(id=presentation_id)
        slides_data = request.POST.get('slides')
        presentation.slides = slides_data.replace('\\"', '"')
        presentation.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def upload_image(request):
    """Загрузка изображения"""
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        image_path = os.path.join(upload_dir, image.name)
        try:
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            image_url = os.path.join(settings.MEDIA_URL, 'uploads', image.name)
            return JsonResponse({'status': 'success', 'url': image_url})
        except IOError as e:
            return JsonResponse({'status': 'ошибка', 'message': f'Ошибка при сохранении файла: {str(e)}'}, status=500)
    return JsonResponse({'status': 'ошибка'}, status=400)

@csrf_exempt
def generate_image(request):
    """Генерация изображения"""
    if request.method == 'POST':
        image_prompt = request.POST.get('image_prompt')
        image_scale = request.POST.get('image_scale')
        image_url = gen(image_prompt, image_scale)

        return JsonResponse({'status': 'success', 'url': image_url})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def re_generate_text(request):
    """Перегенерация текста"""
    if request.method == 'POST':
        text_prompt = request.POST.get('text_prompt')
        text = request.POST.get('text')
        re_generated_text = send_to_change_text(text, text_prompt)
        return JsonResponse({'status': 'success', 'text': re_generated_text})
    return JsonResponse({'status': 'error'}, status=400)

# Функции для работы с комментариями
@csrf_exempt
def add_comment(request, presentation_id):
    """Добавление комментария"""
    if request.method == 'POST':
        presentation = Presentation.objects.get(id=presentation_id)
        comment_text = request.POST.get('comment')
        comments = json.loads(presentation.comments) if presentation.comments else []
        comment = {
            'id': len(comments) + 1,
            'text': comment_text
        }
        comments.append(comment)
        presentation.comments = json.dumps(comments)
        presentation.save()
        return JsonResponse({'status': 'success', 'comment': comment})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def delete_comment(request, presentation_id):
    """Удаление комментария"""
    if request.method == 'POST':
        presentation = Presentation.objects.get(id=presentation_id)
        comment_id = int(request.POST.get('comment_id'))
        comments = json.loads(presentation.comments) if presentation.comments else []
        comments = [comment for comment in comments if comment['id'] != comment_id]
        presentation.comments = json.dumps(comments)
        presentation.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def fix_comment(request, presentation_id):
    """Исправление комментария"""
    if request.method == 'POST':
        presentation = Presentation.objects.get(id=presentation_id)
        comment_text = request.POST.get('comment_text')
        presentation.slides = send_to_proceed_comm(presentation.slides, comment_text)
        print(presentation.slides, comment_text)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
