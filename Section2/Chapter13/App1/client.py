import requests

get_openapi = requests.get(
    "http://127.0.0.1:5000/openapi.json"
)

if get_openapi.status_code == 200:
    document = get_openapi.json()