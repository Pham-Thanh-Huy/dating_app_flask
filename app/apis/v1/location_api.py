from flask import Blueprint, jsonify

from app.utils.request_other_api import get_lat_lng_by_address

location_api = Blueprint('Location', __name__)

