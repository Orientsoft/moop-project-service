from flask import make_response
from bson import ObjectId


def raise_status(status, result=None):
    resp = make_response()
    resp.status_code = status
    resp.headers['content-type'] = 'plain/text'
    if result:
        resp.response = result
    return resp


def filter(query_list=None, updateObj=None, ObjectId_list=None):
    returnObj = {}
    for x in updateObj.keys():
        if x in query_list:
            if ObjectId_list and x in ObjectId_list:
                returnObj[x] = ObjectId(updateObj[x])
            else:
                returnObj[x] = updateObj[x]
    return returnObj
