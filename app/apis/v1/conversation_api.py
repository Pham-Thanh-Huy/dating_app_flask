from email.policy import default

from flask import Blueprint, jsonify, request, make_response

from app.security.security_config import authenticate_api
from app.service.conversation_service import get_conversation_by_id_service, send_message_service, get_list_message_by_user_id_service, unmatch_user_service
from app.utils.constant import Constant

conversation_api = Blueprint('conversation', __name__)


@conversation_api.route("/", defaults={'user_id': None}, methods=['GET'])
@conversation_api.route("/<user_id>", methods=['GET'])
@authenticate_api
def get_conversation_by_id_api(user_id: int):
    if user_id == None:
        return jsonify({'code': '1002', 'message': 'Parameter is not enough'}), 400
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({
            'code': '1003',
            'message': 'Parameter type is invalid'
        }), 400
    response = get_conversation_by_id_service(user_id)
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@conversation_api.route("/message", methods=['POST'])
@authenticate_api
def send_message_api():
    response = send_message_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@conversation_api.route("/message", defaults={'conversation_id': None} , methods=['GET'])
@conversation_api.route("/<conversation_id>/message", methods=['GET'])
@authenticate_api
def get_list_message_by_user_id_api(conversation_id: int):
    user_id = request.args.get("userId")
    if not user_id:
        return make_response({
            "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH,
            "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE
        }, int(Constant.API_STATUS.BAD_REQUEST))
    try:
        user_id = int(user_id)
    except ValueError:
        return make_response({
            "code": Constant.API_STATUS.PARAMETER_TYPE_IS_INVALID,
            "message": Constant.API_STATUS.PARAMETER_TYPE_IS_INVALID_MESSAGE
        }, int(Constant.API_STATUS.BAD_REQUEST))

    if conversation_id == None:
        return jsonify({'code': '1002', 'message': 'Parameter is not enough'}), 400
    try:
        conversation_id = int(conversation_id)
    except ValueError:
        return jsonify({
            'code': '1003',
            'message': 'Parameter type is invalid'
        }), 400


    response = get_list_message_by_user_id_service(conversation_id, user_id)
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@conversation_api.route("/unmatch", methods=['DELETE'])
@authenticate_api
def unmatch_user_api():
    response = unmatch_user_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code