# Generated by Django 4.2.16 on 2024-09-07 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_presentation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='slides',
            field=models.JSONField(default='[\n        {\n            "template": "titleSlide",\n            "content": {\n                "1": "Заголовок",\n            }\n        },\n    ]', verbose_name='Слайды'),
        ),
    ]
