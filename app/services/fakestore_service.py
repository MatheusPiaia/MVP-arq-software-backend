import requests

FAKESTORE_URL = "https://fakestoreapi.com/products"


def fetch_products_from_fakestore():
    response = requests.get(FAKESTORE_URL, timeout=10)
    response.raise_for_status()  # lança erro se falhar
    return response.json()