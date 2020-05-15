class APIException(Exception):
    status_code = 500
    default_detail = "A server error occured"

    def __int__(self, detail=None, errors=None, code=None):
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