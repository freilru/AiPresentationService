# Generated by Django 4.2.16 on 2024-09-06 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_slide_image_url_slide_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slide',
            name='image',
        ),
        migrations.AddField(
            model_name='slide',
            name='image_fon',
            field=models.ImageField(blank=True, null=True, upload_to='slides/', verbose_name='Медиа картинка'),
        ),
        migrations.AddField(
            model_name='slide',
            name='image_title',
            field=models.ImageField(blank=True, null=True, upload_to='slides/', verbose_name='Медиа картинка'),
        ),
    ]
