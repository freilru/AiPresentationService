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
        json_response = response.json()
        json_response = json.loads(json_response['response'])
        json_response = json.dumps(json_response)

        json_response = json_response.replace('\n', '').replace('"', '\"').replace("```", '').replace('fields', 'content')
        return json_response
    except requests.exceptions.RequestException as e:
        print(e)
        return pres



