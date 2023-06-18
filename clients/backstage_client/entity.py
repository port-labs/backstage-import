import requests

from config.config import BACKSTAGE_URL


def get_backstage_entities():
    response = requests.get(f"{BACKSTAGE_URL}/api/catalog/entities")
    response.raise_for_status()

    return response.json()
