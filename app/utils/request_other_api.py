import logging

import requests
from app.utils.constant import Constant

def get_lat_lng_by_address(address: str):
    try:
        param = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "dating-app"
        }

        response = requests.get(Constant.LOCATION_URL, params=param, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            logging.error(f"[ERROR-TO-GET-LAT-LNG] No results found for address: {address}")
            return None

        return data[0]['lat'], data[0]['lon']
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-LAT-LNG] {e}")
        return None