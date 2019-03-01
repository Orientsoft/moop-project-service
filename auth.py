from flask import make_response


def raise_status(status, result=None):
    resp = make_response()
    resp.status_code = status
    resp.headers['content-type'] = 'plain/text'
    if result:
        resp.response = result
    return resp
