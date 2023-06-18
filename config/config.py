import os


PORT_BASE_URL = os.environ.get("PORT_BASE_URL", "https://api.getport.io/v1")
PORT_CLIENT_ID = os.environ.get("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.environ.get("PORT_CLIENT_SECRET")
BACKSTAGE_URL = os.environ.get("BACKSTAGE_URL", "http://localhost:7000")
