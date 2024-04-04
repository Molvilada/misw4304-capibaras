import re
from flask import Blueprint, request, Response, jsonify
from flask.views import MethodView
from models import BlacklistEmail
from .schemas.schemas import ErrorResponseSchema
from .util import class_route

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
        return Response(ErrorResponseSchema().dumps(error), status=401)

    return None


# Validate email format
def is_valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(regex, email):
        return True
    return False


# Class to verify if an email is in the blacklist
@class_route(blp, "/blacklists/<string:email>", methods=['GET'])
class BlacklistEmailVerification(MethodView):
    def get(self, email):
        if not is_valid_email(email):
            return Response("Invalid email format", status=400)

        blacklisted_email = BlacklistEmail.query.filter_by(email=email).first()

        if blacklisted_email:
            is_blacklisted = True
            reason = blacklisted_email.blocked_reason
        else:
            is_blacklisted = False
            reason = "The email is not in the blacklist"

        return jsonify({'is_blacklisted': is_blacklisted, 'reason': reason}), 200
