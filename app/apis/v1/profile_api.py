from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.profile_service import create_profile_service

profile_api = Blueprint("profile_api", __name__)


@profile_api.route("/", methods=['POST'])
@authenticate_api
def create_profile_api():
    response = create_profile_service()
    return jsonify(response), response['code']

