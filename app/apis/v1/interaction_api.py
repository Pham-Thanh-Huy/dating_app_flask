from crypt import methods

from flask import Blueprint, jsonify

from app.security.security_config import authenticate_api
from app.service.interaction_service import add_interaction_service, get_list_interaction_by_user_service

interaction_api = Blueprint('interaction', __name__)


@interaction_api.route('/', methods=['POST'])
def add_interaction_api():
    response = add_interaction_service()
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code


@interaction_api.route('/', defaults={'user_id': None, 'is_like': None}, methods=['GET'])
@interaction_api.route('/<user_id>-<is_like>', methods=['GET'])
@authenticate_api
def get_list_interaction_by_user_api(user_id, is_like):
    if user_id == None or is_like == None:
        return jsonify({'code': '1002', 'message': 'Parameter is not enough'}), 400

    try:
        is_like = int(is_like)
    except ValueError:
        return jsonify({'code': '1004', 'message': 'Parameter value is invalid'}), 400

    if is_like not in (0, 1):
        return jsonify({'code': '1004', 'message': 'Parameter value is invalid'}), 400

    is_like = bool(is_like)

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({
            'code': '1003',
            'message': 'Parameter type is invalid'
        }), 400

    # Tiếp tục xử lý nếu tất cả tham số hợp lệ
    response = get_list_interaction_by_user_service(user_id, is_like)
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code
