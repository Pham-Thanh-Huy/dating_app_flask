from flask import Blueprint, jsonify

from app.service.conversation_service import get_conversation_by_id_service

conversation_api = Blueprint('conversation', __name__)

@conversation_api.route("/<int:user_id>", methods=['GET'])
def get_conversation_by_id_api(user_id: int):
    response = get_conversation_by_id_service(user_id)
    return jsonify(response), response['code']


