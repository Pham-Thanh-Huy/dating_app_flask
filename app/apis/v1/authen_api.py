from flask import Blueprint, request, jsonify

from app.security.security_config import authenticate_api
from app.service.authen_service import register_service, login_service, reset_password_service

authen_api = Blueprint('authen_api', __name__)

@authen_api.route('/register', methods=['POST'])
def register_api():
    response = register_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@authen_api.route('/sign-in', methods=['POST'])
def login_api():
    response = login_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@authen_api.route('reset-password', methods=['POST'])
@authenticate_api
def reset_password_api():
    response = reset_password_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code
