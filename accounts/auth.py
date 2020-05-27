import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from accounts.schema import LoginSchema, RegisterSchema
from accounts.models import UserSession, Account
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError

from common import api_exceptions
from common.helpers import (
    api_token_required,
    generate_random_alphenumeric_number,
    validate_json_request,
)
from common.helpers import make_response, set_request_session
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from marshmallow import ValidationError

User = get_user_model()

@require_http_methods(["POST"])
@api_exceptions.api_exception_handler
@validate_json_request
@method_decorator(csrf_exempt)
def login(request):
    """
    This API is used to login a user in system. Access Token is return per user session.
    """

    schema = LoginSchema()
    response = dict()
    # validate request data
    try:
        data = schema.loads(request.body)
    except ValidationError as e:
        raise api_exceptions.BadRequestData(errors=e.messages)
    print(data)
    # authenticate user in system
    user = authenticate(username=data["username"], password=data["password"])
    if not user:
        raise api_exceptions.BadRequestData(errors="Invalid credentials")

    # generate user session id
    session_id = generate_random_alphenumeric_number(32)
    # get session data

    session = UserSession
    exp_time = settings.JWT_WEB_EXP_DELTA_HOURS
    # if session exists, delete this session and create new one
    session.objects.filter(user=user).delete()

    # create new session for user
    try:
        session.objects.create(user=user, session_id=session_id)
    # # Handling scenario for multiple user creation at same time
    except IntegrityError:
        raise api_exceptions.BadRequestData(errors="Session already exists")

    # read private secret key
    private_key = settings.JWT_SECRET

    # set payload with user id and expiry time
    payload = {
        "user_id": str(user.id),
        "exp": (timezone.now() + timezone.timedelta(hours=exp_time)),
        "session_id": session_id,
    }

    # encode token with private key
    token = jwt.encode(payload, private_key).decode("utf-8")
    response["token"] = token
    response["user_id"] = str(user.id)
    response["account_type"] = user.user_type
    request.user = user
    print(response)
    return JsonResponse(make_response(response, "Successfully logged in", code=201), status=201)

@method_decorator(csrf_exempt)
@require_http_methods(["POST"])
@api_exceptions.api_exception_handler
@api_token_required
def logout(request):
    """
    This API is used to logout the user session from system.
    """
    request.session.delete()
    code = 201
    return JsonResponse(make_response({}, "Successfully logged out", code=code), status=code)

@require_http_methods(["POST"])
@api_exceptions.api_exception_handler
@validate_json_request
@method_decorator(csrf_exempt)
def register(request):
    """
    This API is used to register the user to system.
    """
    schema = RegisterSchema()
    # validate request data
    try:
        data = schema.loads(request.body)
    except ValidationError as e:
        raise api_exceptions.BadRequestData(errors=e.messages)
    user_type_dict = {"user":1, "tagger":2, "reviewer":3}
    data["user_type"] = user_type_dict[data["user_type"]]
    try:
        password = data.pop("password")
        user = Account.objects.create(**data)
        user.set_password(password)
        user.save()
    except (IntegrityError, DjangoValidationError) as e:
        raise api_exceptions.BadRequestData(errors=e.messages)
    return JsonResponse(make_response({}, "Successfully registered user", code=201), status=201)