from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.user_service import delete_account_service
from app.utils.constant import Constant

user_api = Blueprint("user_api", __name__)

@user_api.route("/", defaults={'user_id': None}, methods=['DELETE'])
@user_api.route("/<user_id>", methods=['DELETE'])
@authenticate_api
def delete_account_api(user_id):
    if user_id is None:
        return jsonify({
            "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH,
            "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
        }), 400

    if not str(user_id).isdigit():
        return jsonify({
            "code": Constant.API_STATUS.PARAMETER_TYPE_IS_INVALID,
            "message": Constant.API_STATUS.PARAMETER_TYPE_IS_INVALID_MESSAGE,
        }), 400


    response = delete_account_service(user_id)
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code
