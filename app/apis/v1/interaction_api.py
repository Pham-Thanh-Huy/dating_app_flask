from flask import Blueprint, jsonify

from app.service.interaction_service import add_interaction_service

interaction_api = Blueprint('interaction', __name__)

@interaction_api.route('/', methods=['POST'])
def add_interaction_api():
    response = add_interaction_service()
    return jsonify(response), response['code']