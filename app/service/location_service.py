import logging
from flask import request
from flask_restx import ValidationError
from sqlalchemy.sql.expression import text

from app import db
from app.models import Profile
from app.schema.location_schema import LocationSchema
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response
from app.utils.validate_util import parse_validation_error


def get_list_user_near_by_service():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return {
                "message": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.PARAMETER_IS_NOT_ENOUGH
            }
        schema = LocationSchema()
        schema.load(data)

        query = text("""
                     SELECT *,
                            (6371 * ACOS(
                                    COS(RADIANS(:user_lat)) * COS(RADIANS(CAST(lat AS DECIMAL(10, 6)))) *
                                    COS(RADIANS(CAST(lng AS DECIMAL(10, 6))) - RADIANS(:user_lng)) +
                                    SIN(RADIANS(:user_lat)) * SIN(RADIANS(CAST(lat AS DECIMAL(10, 6))))
                                    )) AS distance
                     FROM location
                     HAVING distance < :radius
                     ORDER BY distance ASC
                     """)

        params = {
            'user_lat': float(data['lat']),
            'user_lng': float(data['lng']),
            'radius': float(data['radius'])
        }

        list_location_nearby = db.session.execute(query, params).fetchall()
        if not list_location_nearby:
            return {
                "message": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA_MESSAGE,
                "http_status_code": Constant.API_STATUS.BAD_REQUEST,
                "code": Constant.API_STATUS.NO_DATA_OR_END_OF_LIST_DATA
            }

        list_profile_nearby = [db.session.query(Profile).filter_by(id=location.profile_id).first() for location in
                               list_location_nearby]
        list_profile_map_to_dict = [profile.to_dict() for profile in list_profile_nearby]
        return {
            "message": Constant.API_STATUS.OK_MESSAGE,
            "http_status_code": Constant.API_STATUS.SUCCESS,
            "code": Constant.API_STATUS.OK,
            "nearby": list_profile_map_to_dict
        }
    except ValidationError as e:
        error_dict = parse_validation_error(e)
        return error_dict
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-LIST-USER-NEAR-BY] {e}")
        return internal_server_error_response()
