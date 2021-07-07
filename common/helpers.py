from . import api_exceptions
import json
from functools import wraps
import hashlib
import json
import random
import string
import time
import jwt
import django.core.exceptions as dj_core_exceptions
from functools import wraps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse

GET_SUCCESS_CODE = 200
POST_SUCCESS_CODE = 201
PUT_SUCCESS_CODE = 202
DELETE_SUCCESS_CODE = 204

INVALID_TOKEN = "Invalid Token"
TOKEN_NOT_PROVIDED = "Token not provided"
AUTH_ERROR = "Authentication error"
USER_NOT_EXIST_IN_ACCOUNT = "User doesn't exist in the system"

def make_response(data, message, code):
    if isinstance(data,list):
        resp_data = {
            "message":message,
            "status_code":code,
            "payload":data
        }
        return resp_data
    elif isinstance(data, dict):
        data["message"] = message
        data["status_code"] = code
        return data

def get_filters(request, filter_params):
    filters = {}
    if isinstance(filter_params,list):
        for key in filter_params:
            if request.GET.get(key):
                filters[key] = request.GET.get(key)
    if isinstance(filter_params, dict):
        for key, val in filter_params.items():
            if request.GET.get(val):
                filters[key] = request.GET.get(val)
    return filters

def validate_json_request(f):
    """
    Validate request json
    :param f:
    :return:
    """
    @wraps(f)
    def func(request, *args, **kwargs):
        if request.method in ["GET", "DELETE"]:
            return f(request, *args, **kwargs)
        if request.body is None:
            return api_exceptions.ParseError(errors="Parser Error")
        try:
            json.loads(request.body)
            return f(request, *args, **kwargs)
        except ValueError:
            raise api_exceptions.ParseError(errors="Parser Error")
    return func

def generate_random_alphenumeric_number(length=6):
    """
    This function would generate a random alphanumeric number using MD5 hash of provided length
    :param length: integer
    :return: random number
    """
    timestamp = int(time.time())
    random_num = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    md5_hash = hashlib.md5((str(timestamp) + random_num).encode("utf-8")).hexdigest()
    return "".join(random.choices(md5_hash, k=length))


def api_token_required(f):
    """
    Request has been verified by using JWT token
    """

    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        request.user = None
        # get jwt token
        jwt_token = request.META.get("HTTP_VB_API_TOKEN", None)
        if jwt_token:
            try:
                # read public key
                public_key = settings.JWT_SECRET
                # decode jwt token
                payload = jwt.decode(jwt_token, public_key)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return JsonResponse({"error": INVALID_TOKEN, "message": AUTH_ERROR, "status_code": 452}, status=401)

            # set user in request
            user_model = get_user_model()
            user = user_model.objects.filter(id=payload["user_id"])
            if not user:
                return JsonResponse(
                    {"error": USER_NOT_EXIST_IN_ACCOUNT, "message": AUTH_ERROR, "status_code": 453}, status=401
                )
            request.user = user[0]
            request.token = jwt_token
            # check if user session exists in system
            try:
                request.session = request.user.user_session
            except dj_core_exceptions.ObjectDoesNotExist:
                return JsonResponse(
                    {"error": USER_NOT_EXIST_IN_ACCOUNT, "message": AUTH_ERROR, "status_code": 453}, status=401
                )
        else:
            return JsonResponse({"error": TOKEN_NOT_PROVIDED, "message": AUTH_ERROR, "status_code": 454}, status=401)
        # check if user account is blocked in system
        return f(request, *args, **kwargs)

    return decorated_function


def set_request_session(f):
    """
    Set platform in request
    """
    @wraps
    def platform(request, *args, **kwargs):
        try:
            _ = json.loads(request.body.decode("utf-8"))
        except ValueError:
            raise api_exceptions.BadRequestData(errors="Bad request data")
        
        from accounts.models import UserSession
        request.session_table = UserSession
        request.session_exp_time = settings.JWT_WEB_EXP_DELTA_HOURS
        return f(request, *args, **kwargs)
    
    return platform
