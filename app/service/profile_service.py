import logging

from flask import request
from marshmallow import ValidationError
from app.models import Profile
from app.schema.create_profile_schema import CreateProfileSchema
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response


def create_profile_service():
    try:
        data = request.json
        schema = CreateProfileSchema()
        schema.load(data)

        profile = Profile

        return None
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-CREATE-PROFILE] {e}")
        return internal_server_error_response()