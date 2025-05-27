from werkzeug import Response
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied, AccessError

import json
import logging
import functools

""" CODE 200 """
# return 200 ok
def output_ok(resp):

    out = json.dumps({
        "data": resp,
        "response_detail": {
            "messages": "Status OK",
            "messages_type": 1,
            "response_code": 200
        }
    })
    
    return Response(out, headers={"Content-Type":"application/json"})

# return 201 created
def output_created(resp):
    out = json.dumps({
        "data": resp,
        "response_detail": {
            "messages": "Status Created",
            "messages_type": 1,
            "response_code": 201
        }
    })
    
    return Response(out, headers={"Content-Type":"application/json"})


""" CODE 300 """
# return multiple data 300
def output_multiple_choices(resp):
    out = json.dumps({
        "data": resp,
        "response_detail": {
            "messages": "Multiple Data Provided",
            "messages_type": 0,
            "response_code": 300
        }
    })
    
    return Response(out, headers={"Content-Type":"application/json"})


""" CODE 400 """
# return 400 bad request
def output_bad_request(resp):
    out = json.dumps({
        "data": resp,
        "response_detail": {
            "messages": "Bad Request",
            "messages_type": 0,
            "response_code": 400
        }
    })
    
    return Response(out, headers={"Content-Type":"application/json"})

# return 401 no authorization
def output_no_authorization(resp):
    out = json.dumps({
        "data": resp,
        "response_detail": {
            "messages": "No Authorization",
            "messages_type": 0,
            "response_code": 401
        }
    })
    
    return Response(out, headers={"Content-Type":"application/json"})

# return 403 Forbidden
def output_forbidden(resp):
    out = json.dumps({
        "data": resp,
        "response_detail": {
            "messages": "Access Denied",
            "messages_type": 0,
            "response_code": 403
        }
    })
    
    return Response(out, headers={"Content-Type":"application/json"})

# return 404 not found
def output_not_found(resp):
    out = json.dumps({
        "data": resp,
        "response_detail": {
            "messages": "Not Found",
            "messages_type": 0,
            "response_code": 404
        }
    })
    
    return Response(out, headers={"Content-Type":"application/json"})

# return 405 method not allowed
def output_no_allowed(resp):
    out = json.dumps({
        "data": resp,
        "response_detail": {
            "messages": "Method Not Allowed",
            "messages_type": 0,
            "response_code": 405
        }
    })
    
    return Response(out, headers={"Content-Type":"application/json"})


