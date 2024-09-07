from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:presentation_id>/', views.edit, name='edit'),
    path('create', views.create, name='create'),
    path('save/<int:presentation_id>/', views.save_presentation, name='save_presentation'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('generate_image/', views.generate_image, name='generate_image'),
    path('re_generate_text/', views.re_generate_text, name='re_generate_text'),
]
