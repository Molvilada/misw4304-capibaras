from flask import Blueprint, request, Response, jsonify
from marshmallow import Schema, fields
from datetime import datetime, timezone
from db import db
from sqlalchemy.exc import DatabaseError
from models.black_list_email import BlacklistEmail
from .util import class_route
from flask.views import MethodView
from flask import request 
from .schemas.schemas import ErrorResponseSchema



class CreateRequestSchema(Schema):
    email = fields.String(required=True)
    app_uuid = fields.String(required=True)
    blocked_reason = fields.String(required=True)


blp = Blueprint("Black List Email", __name__)

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


@class_route(blp, "/blacklists", methods=['POST', 'GET'])
class BlacklistEmailResource(MethodView):
    init_every_request = False
    
    def post(self):
        try:
            emailBlock = CreateRequestSchema().loads(request.data)
        except Exception as ex:
            return Response(str(ex), status=400, mimetype='text/plain')
        
       
        new_blacklist_email = BlacklistEmail(
            email=emailBlock['email'],
            app_uuid=emailBlock['app_uuid'],
            blocked_reason=emailBlock.get('blocked_reason'),
            ip_address=request.remote_addr,
            created_at=datetime.now(timezone.utc).replace(microsecond=0)
        )
                
        try:
            db.session.add(new_blacklist_email)
            db.session.commit()
        except DatabaseError:
            return Response("Error al agregar el email a la lista negra", status=412, mimetype='text/plain')

        
        return jsonify({'message': 'El Email se agregó correctamente'}), 201
    
   