# Generated by Django 4.2.16 on 2024-09-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_slide_image_fon_slide_image_background_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='name_display',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Отображаемое Название слайда'),
        ),
        migrations.AlterField(
            model_name='slide',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Системное Название слайда'),
        ),
    ]