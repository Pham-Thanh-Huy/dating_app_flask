from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.profile_service import create_profile_service, update_profile_service, get_profile_by_user_id_service, \
    update_image_profile_service
from app.utils.constant import Constant

profile_api = Blueprint("profile_api", __name__)


@profile_api.route("/", methods=['POST'])
@authenticate_api
def create_profile_api():
    response = create_profile_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code

@profile_api.route("/", methods=['PUT'])
@authenticate_api
def update_profile_api():
    response = update_profile_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code

@profile_api.route("/", defaults={'user_id': None}, methods=['GET'])
@profile_api.route("/<user_id>", methods=['GET'])
@authenticate_api
def get_profile_by_user_id_api(user_id):
    if user_id is None:
        return jsonify({
            "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH,
            "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
        }), 400
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({
            'code': '1003',
            'message': 'Parameter type is invalid'
        }), 400

    response = get_profile_by_user_id_service(user_id)
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@profile_api.route("/images", methods=['PUT'])
@authenticate_api
def update_image_profile_api():
    response = update_image_profile_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code

