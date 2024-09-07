from django.db import models
from django.contrib.auth.models import User

class Theme(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название темы")
    image_title = models.ImageField(upload_to='themes/', verbose_name="Превью темы", null=True, blank=True)
    slides_json = models.JSONField(verbose_name="Слайды", null=True, blank=True)

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return self.name

class Slide(models.Model):
    name = models.CharField(max_length=255, verbose_name="Системное Название слайда", null=True, blank=True)
    name_display = models.CharField(max_length=255, verbose_name="Отображаемое Название слайда", null=True, blank=True)
    html = models.TextField(verbose_name="HTML содержимое слайда")
    index = models.IntegerField(verbose_name="Порядковый номер слайда")
    image_title = models.ImageField(upload_to='slides/', verbose_name="Превью", null=True, blank=True)
    image_background = models.ImageField(upload_to='slides/', verbose_name="Фон слайда", null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тема")

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"
        ordering = ['index']

    def __str__(self):
        return f"Слайд {self.index}"

class Presentation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=255, verbose_name="Название презентации")
    slides = models.JSONField(verbose_name="Слайды", null=True, blank=True)
    comments = models.JSONField(verbose_name="Комментарии", null=True, blank=True)

    class Meta:
        verbose_name = "Презентация"
        verbose_name_plural = "Презентации"

    def __str__(self):
        return self.name
