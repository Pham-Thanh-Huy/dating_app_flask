import logging
from flask import request
from flask_restx import ValidationError
from sqlalchemy.sql.expression import text

from app import db
from app.models import Profile
from app.schema.location_schema import LocationSchema
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response


def get_list_user_near_by_service():
    try:
        data = request.get_json()
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
                "message": f"Không có user nào hiện tại  gần trong bán kính {data['radius']}km!",
                "code": Constant.API_STATUS.FORBIDDEN
            }

        list_profile_nearby = [db.session.query(Profile).filter_by(id=location.profile_id).first() for location in
                               list_location_nearby]
        list_profile_map_to_dict = [profile.to_dict() for profile in list_profile_nearby]
        return {
            "message": Constant.API_STATUS.SUCCESS_MESSAGE,
            "code": Constant.API_STATUS.SUCCESS,
            "nearby": list_profile_map_to_dict
        }
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-LIST-USER-NEAR-BY] {e}")
        return internal_server_error_response()
