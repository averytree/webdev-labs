from flask import Response, request
from flask_restful import Resource
from models import User
from . import get_authorized_user_ids
import json

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        following = get_authorized_user_ids(self.current_user)
        suggestions = User.query.filter(~User.id.in_(following)).limit(7).all()
        sug_data = [user.to_dict() for user in suggestions]
        return Response(json.dumps(sug_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
