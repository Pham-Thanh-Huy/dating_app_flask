from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.block_service import block_user_service, get_list_block_service

block_api=Blueprint('Block', __name__)

@block_api.route('/', methods=['POST'])
@authenticate_api
def block_user_api():
    response = block_user_service()
    return jsonify(response), response['code']


@block_api.route('/', methods=['GET'])
@authenticate_api
def get_list_block_api():
    response = get_list_block_service()
    return jsonify(response), response['code']