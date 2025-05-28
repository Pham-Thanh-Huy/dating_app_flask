from flask import Blueprint, jsonify, request, make_response

from app.security.security_config import authenticate_api
from app.service.conversation_service import get_conversation_by_id_service, send_message_service, \
    get_list_message_by_user_id_service
from app.utils.constant import Constant

conversation_api = Blueprint('conversation', __name__)


@conversation_api.route("/<int:user_id>", methods=['GET'])
@authenticate_api
def get_conversation_by_id_api(user_id: int):
    response = get_conversation_by_id_service(user_id)
    return jsonify(response), response['code']


@conversation_api.route("/message", methods=['POST'])
@authenticate_api
def send_message_api():
    response = send_message_service()
    return jsonify(response), response['code']


@conversation_api.route("/<int:conversation_id>/message", methods=['GET'])
@authenticate_api
def get_list_message_by_user_id_api(conversation_id: int):
    user_id = request.args.get("userId")
    if not user_id:
        return make_response({
            "code": Constant.API_STATUS.BAD_REQUEST,
            "message": "Vui lòng truyền param userId"
        }, Constant.API_STATUS.BAD_REQUEST)
    try:
        user_id = int(user_id)
    except ValueError:
        return make_response({
            "code": Constant.API_STATUS.BAD_REQUEST,
            "message": "userId phải là số nguyên"
        }, Constant.API_STATUS.BAD_REQUEST)
    response = get_list_message_by_user_id_service(conversation_id, user_id)
    return jsonify(response), response['code']
