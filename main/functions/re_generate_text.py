import requests
import json

def re_generate(prompt, text):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer t1.9euelZqQncnHypPNycaXnp3OnceMie3rnpWaj8mclJuVlIzKmpmYk8qKiZHl8_d4EA5J-e9BKRMs_N3z9zg_C0n570EpEyz8zef1656VmpaRyseSypTGlsmNj8uXyYmJ7_zF656VmpaRyseSypTGlsmNj8uXyYmJ.64ySfdJYeYnuat1kLe8deF_m-nvYuaPurFTZDIaSR8kWWwf2iqpWSBM4ZgxhESlZOlUmJpwAStennxEedhGNBw"
    }
    
    payload = {
        "modelUri": "gpt://b1g72uajlds114mlufqi/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": "100"
        },
        "messages": [
            {
                "role": "system",
                "text": prompt
            },
            {
                "role": "user",
                "text": text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    ans = result['result']['alternatives'][0]['message']['text']
    ans = ans.replace('*', '').replace('_', '').replace('`', '').replace('#', '')
    
    return ans