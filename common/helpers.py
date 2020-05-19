
GET_SUCCESS_CODE = 200
POST_SUCCESS_CODE = 201
PUT_SUCCESS_CODE = 202

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