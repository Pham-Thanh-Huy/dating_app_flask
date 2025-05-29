import logging

import jwt, datetime

from app.config import Config
from app.utils.constant import Constant


def generation_token(username):
    payload = {
        'user': username,
        'exp': datetime.datetime.now() + datetime.timedelta(hours=4)
    }
    exp = payload['exp']
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

    return token, exp


def verify_token(token):
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
        return data, None
    except jwt.ExpiredSignatureError:
        return None, Constant.TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return None, Constant.TOKEN_INVALID


def parse_token_get_username(token):
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
        return data['user'], False
    except Exception as e:
        logging.error(f"ERROR-TO-PARSE-TOKEN-JWT: {e}")
        return Constant.ERROR_TO_PARSE_TOKEN, True

