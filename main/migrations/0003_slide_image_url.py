# Generated by Django 4.2.16 on 2024-09-06 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_slide_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='image_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL изображения слайда'),
        ),
    ]
