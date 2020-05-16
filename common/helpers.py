
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