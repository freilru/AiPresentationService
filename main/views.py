from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Slide, Presentation
from .forms import PresentationForm
import json
import os
from django.conf import settings
from main.functions.image import *
from main.functions.re_generate_text import re_generate

def index(request):
    presentation = Presentation.objects.first()  # Получаем первую презентацию
    slides = json.loads(presentation.slides) if presentation else []
    return render(request, 'index.html', {'slides': slides, 'presentation': presentation})

def edit(request, presentation_id):
    presentation = Presentation.objects.get(id=presentation_id)
    slides = Slide.objects.all().order_by('index')
    instance = json.loads(presentation.slides)

    return render(request, 'index.html', {'presentation': presentation, 'slides': slides, 'instance': instance})

def create(request):
    if request.method == 'POST':
        form = PresentationForm(request.POST)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.user = request.user
            presentation.slides = '''[{\"template\":\"bentoGrid\",\"content\":{\"1\":\"Самый технологичнй ЖК во всей Москве\",\"2\":\"Зарядки для элоектромобилей\",\"3\":\"Система Умный Дом\",\"4\":\"Оборудованная территория\",\"5\":\"ИИ Консьерж\",\"img-0\":\"http://127.0.0.1:8000/media/uploads/fote.png\",\"img-1\":\"https://cropas.by/wp-content/uploads/2023/02/yandex1.png\",\"img-2\":\"https://via.placeholder.com/150\",\"img-3\":\"http://127.0.0.1:8000/media/uploads/slide2.png\",\"img-4\":\"http://127.0.0.1:8000/media/uploads/slide6.png\"}},{\"template\":\"titleSlide\",\"content\":{\"1\":\"Pffe\"}}]"'''
            presentation.save()
            return redirect('edit', presentation_id=presentation.id)
    else:
        form = PresentationForm()
    return render(request, 'create.html', {'form': form})

@csrf_exempt
def save_presentation(request, presentation_id):
    if request.method == 'POST':
        presentation = Presentation.objects.get(id=presentation_id)
        slides_data = request.POST.get('slides')
        presentation.slides = slides_data.replace('\\"', '"')
        presentation.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def upload_image(request):
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
    if request.method == 'POST':
        image_prompt = request.POST.get('image_prompt')
        image_scale = request.POST.get('image_scale')
        image_url = gen(image_prompt, image_scale)

        return JsonResponse({'status': 'success', 'url': image_url})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def re_generate_text(request):
    if request.method == 'POST':
        text_prompt = request.POST.get('text_prompt')
        text = request.POST.get('text')
        re_generated_text = re_generate(text_prompt, text)
        return JsonResponse({'status': 'success', 'text': re_generated_text})
    return JsonResponse({'status': 'error'}, status=400)