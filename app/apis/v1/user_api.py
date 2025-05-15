from flask import Blueprint

from app.security.security_config import authenticate_api

user_api = Blueprint("user_api", __name__)

@user_api.route("/<userId>", methods=['DELETE'])
@authenticate_api
def delete_account():
    return None