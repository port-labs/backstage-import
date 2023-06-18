from clients.port_client.common import get_required_headers
from config.config import PORT_BASE_URL

import requests


def create_blueprint(blueprint):
    response = requests.post(
        f"{PORT_BASE_URL}/blueprints", json=blueprint, headers=get_required_headers())

    if response.status_code >= 400 and response.status_code != 409:
        response.raise_for_status()


def update_blueprint(blueprint):
    response = requests.put(
        f"{PORT_BASE_URL}/blueprints/{blueprint['identifier']}", json=blueprint, headers=get_required_headers())

    response.raise_for_status()
