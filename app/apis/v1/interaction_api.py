from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.interaction_service import add_interaction_service, get_list_interaction_by_user_service

interaction_api = Blueprint('interaction', __name__)


@interaction_api.route('/', methods=['POST'])
def add_interaction_api():
    response = add_interaction_service()
    return jsonify(response), response['code']


@interaction_api.route('/<int:user_id>-<int:is_like>', methods=['GET'])
@authenticate_api
def get_list_interaction_by_user_api(user_id, is_like):
    if is_like not in (0, 1):
        return jsonify({'code': 400, 'message': 'is_like phải là 0 hoặc 1'}), 400
    is_like = bool(is_like)
    response = get_list_interaction_by_user_service(user_id, is_like)
    return jsonify(response), response['code']
