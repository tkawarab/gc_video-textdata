from functools import wraps
from typing import Callable, Dict, TypeVar

import firebase_admin
from firebase_admin import auth  # noqa: F401
from flask import request, Response
import structlog


a = TypeVar("a")

default_app = firebase_admin.initialize_app()

def jwt_authenticated(func: Callable[..., int]) -> Callable[..., int]:
    @wraps(func)
    def decorated_function(*args: a, **kwargs: a) -> a:
        header = request.headers.get("Authorization", None)
        if header:
            token = header.split(" ")[1]
            try:
                decoded_token = firebase_admin.auth.verify_id_token(token)
                email = decoded_token["email"]
                
                if not email=="" and not email=="": # add your email here
                    print("access_user:" + email + " denied")
                    return Response(status=401)
                else:
                    print("access_user:" + email + " ok")
            except Exception as e:
                # logger.exception(e)
                print(e)
                return Response(status=403, response=f"Error with authentication: {e}")
        else:
            return Response(status=401)

        request.uid = decoded_token["uid"]
        kwargs['uid'] = decoded_token["uid"]
        kwargs['email'] = email
        return func(*args, **kwargs)

    return decorated_function
