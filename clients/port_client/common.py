import requests

from config.config import PORT_BASE_URL, PORT_CLIENT_ID, PORT_CLIENT_SECRET


def get_required_headers():
    credentials = {'clientId': PORT_CLIENT_ID,
                   'clientSecret': PORT_CLIENT_SECRET}

    token_response = requests.post(
        f'{PORT_BASE_URL}/auth/access_token', json=credentials)

    access_token = token_response.json()['accessToken']
    return {
        'Authorization': f'Bearer {access_token}'
    }
