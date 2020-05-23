import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from accounts.schema import LoginSchema

from common import api_exceptions
from common.helpers import (
    api_token_required,
    generate_random_alphenumeric_number,
    validate_json_request,
)
from common.helpers import make_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from marshmallow import ValidationError

User = get_user_model()

@method_decorator(csrf_exempt)
@require_http_methods(["POST"])
@api_exceptions.api_exception_handler
@validate_json_request
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
    session = request.session_table
    exp_time = request.session_exp_time
    # if session exists, delete this session and create new one
    session.objects.filter(user=user).delete()

    # create new session for user
    try:
        session.objects.create(user=user, session_id=session_id)
    # Handling scenario for multiple user creation at same time
    except IntegrityError:
        raise api_exceptions.BadRequestData(errors="Session already exists")

    # read private secret key
    private_key = open(settings.JWT_PRIVATE_KEY).read()

    # set payload with user id and expiry time
    payload = {
        "user_id": str(user.id),
        "exp": (timezone.now() + timezone.timedelta(hours=exp_time)),
        "session_id": session_id,
    }

    # encode token with private key
    token = jwt.encode(payload, private_key, algorithm=settings.JWT_ALGORITHM).decode("utf-8")
    response["token"] = token
    response["user_id"] = str(user.id)
    response["language"] = user.language
    response["account_number"] = user.account.account_number
    response["account_type"] = user.account.account_type.name
    request.user = user
    return JsonResponse(make_response(request, "Successfully logged in", response), status=201)


@require_http_methods(["POST"])
@api_exceptions.api_exception_handler
@api_token_required
def logout(request):
    """
    This API is used to logout the user session from system.
    """
    request.session.delete()
    code = 201
    return JsonResponse(make_response(request, "Successfully logged out", code=code), status=code)