from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.block_service import block_user_service, get_list_block_service, unblock_user_service
from app.utils.constant import Constant

block_api=Blueprint('Block', __name__)

@block_api.route('/', methods=['POST'])
@authenticate_api
def block_user_api():
    response = block_user_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@block_api.route('/', methods=['GET'])
@authenticate_api
def get_list_block_api():
    response = get_list_block_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@block_api.route('/', defaults={'block_user_id': None}, methods=['DELETE'])
@block_api.route('/<block_user_id>', methods=['DELETE'])
@authenticate_api
def unblock_user_api(block_user_id: int):
    if block_user_id is None:
        return jsonify({
            "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH,
            "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
        }), 400
    try:
        block_user_id = int(block_user_id)
    except ValueError:
        return jsonify({'code': '1004', 'message': 'Parameter value is invalid'}), 400

    response = unblock_user_service(block_user_id)
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code

