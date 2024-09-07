from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('edit/<int:presentation_id>/', views.edit, name='edit'),
    
    # Операции с презентациями
    path('save/<int:presentation_id>/', views.save_presentation, name='save_presentation'),
    
    # Работа с изображениями
    path('upload_image/', views.upload_image, name='upload_image'),
    path('generate_image/', views.generate_image, name='generate_image'),
    
    # Генерация текста
    path('re_generate_text/', views.re_generate_text, name='re_generate_text'),
    
    # Управление комментариями
    path('add_comment/<int:presentation_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:presentation_id>/', views.delete_comment, name='delete_comment'),
    path('fix_comment/<int:presentation_id>/', views.fix_comment, name='fix_comment'),
]
