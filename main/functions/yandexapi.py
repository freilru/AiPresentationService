import requests
import json

# Base URL for your server
BASE_URL = "https://xyandex.pythonanywhere.com"


# Function to send a request to 'gen_pres' endpoint
def send_to_gen_pres(doc, pres):
    url = f"{BASE_URL}/gen_pres"
    payload = {"doc": doc, "pres": pres}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        json_response = response.json()
        json_response = json.loads(json_response['response'])
        json_response = json.dumps(json_response)

        json_response = json_response.replace('\n', '').replace('"', '\"').replace("```", '').replace('fields', 'content')
        return json_response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# Function to send a request to 'change_text' endpoint
def send_to_change_text(text, prompt):
    url = f"{BASE_URL}/change_text"
    payload = {"text": text, "prompt": prompt}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        json_response = response.json()
        return json.loads(json_response['response'])['text']
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# Function to send a request to 'proceed_comm' endpoint
def send_to_proceed_comm(pres, comm):
    url = f"{BASE_URL}/proceed_comm"
    payload = {"pres": pres, "comm": comm}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        json_response = response['response']['text']
        json_response = json_response[json_response.index('['):json_response.rindex(']')+1]
        json_response = json_response.replace('\n', '').replace('"', '\"').replace("```", '').replace('fields', 'content')
        return json.loads(json_response)
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# Example usage of the functions
if __name__ == "__main__":
    # Example input for each function
    doc_example = "Огромный документ"
    text_example = "Здарова работяги"
    prompt_example = "Сделай более профессиональным"
    pres = "[]"
    pres_example = "[{\"template\":\"bentoGrid\",\"content\":{\"1\":\"Самый технологичный жилой комплекс во всей Москве\",\"2\":\"Зарядки для электромобилей.\",\"3\":\"Система «Умный дом».\",\"4\":\"Зона с оборудованием\",\"5\":\"ИИ Консьерж\",\"img-0\":\"http://127.0.0.1:8000/media/generated_images/generated_image_58586161-3854-4021-a64d-df08b35fdb18.png\",\"img-1\":\"http://127.0.0.1:8000/media/generated_images/generated_image_de381578-7ad0-48fb-9558-3fadf02a6534.png\",\"img-2\":\"http://127.0.0.1:8000/media/generated_images/generated_image_a434d053-2904-40cc-b8f6-63c7ec186ad6.png\",\"img-3\":\"http://127.0.0.1:8000/media/uploads/slide2.png\",\"img-4\":\"http://127.0.0.1:8000/media/uploads/slide6.png\"}},{\"template\":\"titleSlide\",\"content\":{\"1\":\"Название презентации\"}}]"
    comm_example = "Переведи первый слайд на английский"

    # Send requests to each endpoint
    print("Sending to gen_pres:")
    print(send_to_gen_pres(doc_example, pres))

    print("\nSending to change_text:")
    print(send_to_change_text(text_example, prompt_example))

    print("\nSending to proceed_comm:")
    print(send_to_proceed_comm(pres_example, comm_example))
