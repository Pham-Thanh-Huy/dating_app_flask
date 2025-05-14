from flask import Blueprint, request, jsonify
from app.service.authen_service import register_service, login_service

authen_api = Blueprint('authen_api', __name__)

@authen_api.route('/register', methods=['POST'])
def register_api():
    response = register_service()
    return jsonify(response), response['code']


@authen_api.route('/login', methods=['POST'])
def login_api():
    response = login_service()
    return jsonify(response), response['code']

