from flask import Blueprint, jsonify

from app.utils.request_other_api import get_lat_lng_by_address

location_api = Blueprint('Location', __name__)


@location_api.route('/', methods=['GET'])
def test():
    result = get_lat_lng_by_address("K5 Bach Khoa Hai Bà Trưng Hà Nội")
    if result is not None:
        lat, lng = result
        return jsonify({"lat": lat, "lng": "lng"}), 200

    return jsonify({"error": "lay toa do khong thanh cong"}), 200