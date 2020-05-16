from functools import wraps
from django.http import JsonResponse
from django.utils.encoding import force_text

def api_exception_handler(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except APIException as e:
            # api exceptions are of string typed error
            if isinstance(e.errors, str):
                error = e.errors

            # check if error is of dict type
            elif isinstance(e.errors, dict):
                error = dict()
                for k, v in e.errors.items():
                    # error can be dict of dict
                    if isinstance(v, dict):
                        # this error type handling nested schema, reference: check for register account errors
                        error.update(
                            {
                                str(k).lower(): {
                                    str(m).lower(): e[0] if isinstance(e, list) else e for m, e in v.items()
                                }
                            }
                        )

                    # if error dict values contains list , errors used every where in schema
                    else:
                        error.update({str(k).lower(): v[0] if isinstance(v, list) else v})

            # if something unexpected happened
            else:
                error = e.errors
            return JsonResponse({"message": str(e.detail), "error": error, "status_code": e.code}, status=e.code)

    return decorated_function

class APIException(Exception):
    status_code = 500
    default_detail = "A server error occured"

    def __init__(self, detail=None, errors=None, code=None):
        self.detail = self.default_detail if detail==None else detail
        self.errors = errors
        self.code = self.status_code if code==None else code
    
    def __str__(self):
        return self.detail

class BadRequestData(APIException):
    status_code = 400
    default_detail = "Bad request"

class ParseError(APIException):
    status_code = 400
    default_detail = "Malformed request"

class AuthenticationFailed(APIException):
    status_code = 401
    default_detail = "Authentication error"

class NotAuthenticated(APIException):
    status_code = 401
    default_detail = "Not authenticated"

class PermissionDenied(APIException):
    status_code = 403
    default_detail = "Permission denied"

class NotFound(APIException):
    status_code = 404
    default_detail = "Not found"

class NotAcceptable(APIException):
    status_code = 406
    default_detail = "Could not satisfy the request"

class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Server is Unavailable"

class NotImplemented(APIException):
    status_code = 501
    default_detail = "Server doesn't support the functionality"

class DuplicateResource(APIException):
    status_code = 409
    default_detail = "Resource already exists"

class ResourceInMutualExclusionZone(APIException):
    status_code = 409
    default_detail = "Read and write not allowed"

class UnProcessableResource(APIException):
    status_code = 422
    default_detail = "Resource unprocessable"

class ImproperlyConfigured(APIException):
    status_code = 500
    default_detail = "Improperly configured"

class ValidationError(APIException):
    status_code = 400
    default_detail = "Bad request"