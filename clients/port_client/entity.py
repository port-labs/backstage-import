import requests

from config.config import PORT_BASE_URL
from clients.port_client.common import get_required_headers


def create_entity(blueprint, entity):
    print(f"Creating {blueprint} {entity['identifier']}")

    response = requests.post(
        f"{PORT_BASE_URL}/blueprints/{blueprint}/entities?create_missing_related_entities=true&upsert=true&merge=true",
        json=entity,
        headers=get_required_headers()
    )
    if response.status_code != 200:
        print(response.json())

    response.raise_for_status()
