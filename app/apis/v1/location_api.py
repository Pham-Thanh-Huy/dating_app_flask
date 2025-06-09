from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.location_service import get_list_user_near_by_service
from app.utils.request_other_api import get_lat_lng_by_address

location_api = Blueprint('Location', __name__)


@location_api.route('/nearby', methods=['GET'])
@authenticate_api
def get_list_user_near_by_api():
    response = get_list_user_near_by_service()
    code = int(response['code'])
    return jsonify(response), code
