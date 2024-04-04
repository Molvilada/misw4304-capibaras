import requests
from flask import Blueprint, request, Response, jsonify, g, abort
from flask.views import MethodView

from .schemas.schemas import ErrorResponseSchema
from .util import class_route
from db import db
from models import BlacklistEmail

# Blueprint for the blacklists
blp = Blueprint("Black List Email Verification", __name__)

# Bearer token to access the endpoint
bearer_token = 'Bearer VerifyToken1234'


# Verify the token
@blp.before_request
def verify_token():
    token = request.headers.get('Authorization')

    if not token:
        error = {"msg": "Token is required"}
        return Response(ErrorResponseSchema().dumps(error), status=403)

    if token != bearer_token:
        error = {"msg": "Invalid token"}
        return Response(ErrorResponseSchema().dumps(error), status=403)

    return None


# Class to verify if an email is in the blacklist
@class_route(blp, "/blacklists/<string:email>", methods=['GET'])
class BlacklistEmailVerification(MethodView):
    def get(self, email):
        return jsonify({'melo': "sisas"}), 200
