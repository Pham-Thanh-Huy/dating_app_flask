import logging
from flask import request
from flask_restx import ValidationError
from sqlalchemy.sql.expression import text

from app import db
from app.models import Location
from app.schema.location_schema import LocationSchema
from app.utils.constant import Constant
from app.utils.response_util import internal_server_error_response


def get_list_user_near_by():
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

        return None
    except ValidationError as e:
        return {
            "message": e.messages,
            "code": Constant.API_STATUS.BAD_REQUEST
        }
    except Exception as e:
        logging.error(f"[ERROR-TO-GET-LIST-USER-NEAR-BY] {e}")
        return internal_server_error_response()
