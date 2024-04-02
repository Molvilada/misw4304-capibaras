from flask import Blueprint, Response
from flask.views import MethodView
from .util import class_route

blp = Blueprint("Health Check", __name__)

@class_route(blp, "/health")
class HealthCheck(MethodView):
    init_every_request = False

    def get(self):
        return Response("Healthy", status=200, mimetype='text/plain')
