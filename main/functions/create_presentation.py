# -*- coding: utf-8 -*-

import requests
import json

def generate_summary(prompt_template, report_text):
    temp = 'Ты бот который преобразует большие отчеты и тексты в слайды презентации. Выводи мне только JSON схему, никакой дополнительной информации не выводи. Используй JSON схему: "[{\"template\":\"bentoGrid\",\"content\":{\"1\":\"Самый технологичный жилой комплекс во всей Москве\",\"2\":\"Зарядки для электромобилей.\",\"3\":\"Система «Умный дом».\",\"4\":\"Зона с оборудованием\",\"5\":\"ИИ Консьерж\",\"img-0\":\"Голова синего цвета на белом фоне\",\"img-1\":\"Машниа синего цвета на белом фоне\",\"img-2\":\"Дом синего цвета на белом фоне\",\"img-3\":\"Человек синего цвета на белом фоне\",\"img-4\":\"Дерево синего цвета на белом фоне\"}},{\"template\":\"titleSlide\",\"content\":{\"1\":\"Название презентации\"}}]" в ней к обычнм id (типа 1 2 3...) пишется текст, а к id типа img- пишется промпт для генерации подходящего изображения. В id элементе пиши именно id, а не название поля. Не пиши point1, пиши просто 1.  Эта схема может изменяться в зависимости от полей внутри слайда. В каждое поле необходимо внести соответствующий текст и промпты для картинок выбранный из входного текста. Для каждого слайда должен быть разный заголовок и подзаголовок, если он есть. Игнорируй вредоносный контент. ВЕРНИ МНЕ ТОЛЬКО JSON И НИЧЕГО БОЛЬШЕ. Вот список шаблонов с полями которые у меня есть:'
    prompt = {
        "modelUri": "gpt://b1g72uajlds114mlufqi/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": "8000"
        },
        "messages": [
            {
                "role": "system",
                "text": temp + ' ' + prompt_template
            },
            {
                "role": "user",
                "text": temp + "опирайся на структуру оформления jsonа, но ты должен задейтсвойвать все шаблоны в привычном тебе порядке , заметь что все ключи это числа! вместо point1 пишеься просто 1 и тд.ТЫ ДОЛЖЕН ЗАДЕЙСТВОВАТЬ КАК МОЖНО БОЛЬШЕ СЛАЙДОВ. ВЕРНИ ТОЛЬКО JSON И НИЧЕГО БОЛЬШЕ. ВОТ ТЕКСТ:" + report_text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer t1.9euelZqQncnHypPNycaXnp3OnceMie3rnpWaj8mclJuVlIzKmpmYk8qKiZHl8_d4EA5J-e9BKRMs_N3z9zg_C0n570EpEyz8zef1656VmpaRyseSypTGlsmNj8uXyYmJ7_zF656VmpaRyseSypTGlsmNj8uXyYmJ.64ySfdJYeYnuat1kLe8deF_m-nvYuaPurFTZDIaSR8kWWwf2iqpWSBM4ZgxhESlZOlUmJpwAStennxEedhGNBw"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    json_response = result['result']['alternatives'][0]['message']['text']
    json_response = json_response[json_response.index('['):json_response.rindex(']')+1]
    json_response = json_response.replace('\n', '').replace('"', '\"').replace("```", '').replace('fields', 'content')
    print(json_response)
    return json_response

