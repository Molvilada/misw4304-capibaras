from importlib.resources import Resource
from sqlalchemy.exc import DatabaseError
from flask import Blueprint, request, Response, jsonify, g

from models.black_list_email import BlacklistEmail
from .util import class_route
from marshmallow import Schema, fields
from datetime import datetime, timezone
from db import db


blp = Blueprint("black_list_email", __name__)

class CreateRequestSchema(Schema):
    email = fields.String(required=True)
    app_uuid = fields.String(required=True)
    blocked_reason = fields.String(required=True)
    ip_address = fields.String(required=True)
    

@class_route(blp, "/blacklists")
class BlacklistEmailResource(Resource):
    def post(self):
        try:
            emailBlock = CreateRequestSchema().loads(request.data)
        except Exception as ex:
            return Response(str(ex), status=400, mimetype='text/plain')
        
       
        new_blacklist_email = BlacklistEmail(emailBlock.email, emailBlock.app_uuid, emailBlock.blocked_reason, emailBlock.ip_address,  datetime.now(timezone.utc).replace(microsecond=0))
        
        try:
            db.session.add(new_blacklist_email)
            db.session.commit()
        except DatabaseError:
            return Response("Error al agregar el email a la lista negra", status=412, mimetype='text/plain')

        
        return jsonify({'message': 'El Email se agrego correctamente'}), 201
    
   