from rest_framework.views import exception_handler


def status_code_handler(exec,context):
    resp =  exception_handler(exec,context)

    if resp is not None and resp.status_code == 403:
        resp.status_code = 401
    return resp