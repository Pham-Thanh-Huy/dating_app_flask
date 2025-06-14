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
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code

@notification_api.route('/',defaults={'id':None}, methods=['DELETE'])
@notification_api.route('/<id>', methods=['DELETE'])
@authenticate_api
def delete_notification_api(id: int):
    if id is None:
        return jsonify({
            "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH,
            "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
        }), 400
    try:
        id = int(id)
    except ValueError:
        return jsonify({'code': '1004', 'message': 'Parameter value is invalid'}), 400

    response = delete_notification_service(id)
    code = int(response.pop("http_status_code", 200))
    return jsonify(response), code
