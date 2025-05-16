from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.user_service import delete_account_service

user_api = Blueprint("user_api", __name__)

@user_api.route("/<user_id>", methods=['DELETE'])
@authenticate_api
def delete_account_api(user_id):
    response = delete_account_service(user_id)
    return jsonify(response), response['code']
