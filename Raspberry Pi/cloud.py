import requests
from dotenv import dotenv_values


def send_data(data: int) -> bool:
    CONFIG = dotenv_values(".env")
    api_key = CONFIG["API_KEY"]
    url = "https://api.thingspeak.com/update.json"
    body = {"api_key": api_key, "field1": data}
    try:
        response = requests.get(url, json=body)
    except requests.exceptions.ConnectionError:
        return False
    return response.status_code == 200
