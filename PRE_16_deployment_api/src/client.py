"""Consume la API de predicción desde otro proceso."""

import requests

API_URL = "http://127.0.0.1:8000/predict"


def make_request(api_url=API_URL):
    raise NotImplementedError


if __name__ == "__main__":
    print(make_request())
