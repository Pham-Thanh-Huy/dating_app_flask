from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.profile_service import create_profile_service, update_profile_service, get_profile_by_user_id_service, \
    update_image_profile_service

profile_api = Blueprint("profile_api", __name__)


@profile_api.route("/", methods=['POST'])
@authenticate_api
def create_profile_api():
    response = create_profile_service()
    return jsonify(response), response['code']

@profile_api.route("/", methods=['PUT'])
@authenticate_api
def update_profile_api():
    response = update_profile_service()
    return jsonify(response), response['code']


@profile_api.route("/<int:user_id>", methods=['GET'])
@authenticate_api
def get_profile_by_user_id_api(user_id):
    response = get_profile_by_user_id_service(user_id)
    return jsonify(response), response['code']


@profile_api.route("/images", methods=['PUT'])
@authenticate_api
def update_image_profile_api():
    response = update_image_profile_service()
    return jsonify(response), response['code']

