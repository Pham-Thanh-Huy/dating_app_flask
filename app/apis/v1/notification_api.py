from flask import Blueprint, make_response, request, jsonify

from app.security.security_config import authenticate_api
from app.service.notification_service import get_notification_service, delete_notification_service
from app.utils.constant import Constant
from app.utils.validate_util import validate_param_type_int

notification_api = Blueprint('Notification', __name__)


@notification_api.route('/', methods=['GET'])
@authenticate_api
def get_notification_api():
    user_id = request.args.get("userId")
    index = request.args.get("index")
    count = request.args.get("count")

    # --> CHANGE TYPE TO INT IF NOT FOUND FUNCTION HAS VALIDATED !
    user_id, err = validate_param_type_int("userId", user_id)
    if err:
        return err

    index, err = validate_param_type_int("index", index)
    if err:
        return err

    count, err = validate_param_type_int("count", count)
    if err:
        return err

    response = get_notification_service(user_id, index, count)
    code = int(response['code'])
    return jsonify(response), code

@notification_api.route('/<int:id>', methods=['DELETE'])
@authenticate_api
def delete_notification_api(id: int):
    response = delete_notification_service(id)
    code = int(response['code'])
    return jsonify(response), code
