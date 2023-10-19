import requests

from config.config import BACKSTAGE_URL, BACKSTAGE_BEARER_TOKEN


def get_backstage_entities():
    headers = {"Authorization": f"Bearer {BACKSTAGE_BEARER_TOKEN}"} if BACKSTAGE_BEARER_TOKEN else {}
    response = requests.get(f"{BACKSTAGE_URL}/api/catalog/entities", headers=headers)
    response.raise_for_status()

    return response.json()
