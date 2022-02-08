from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json
from my_decorators import handle_db_insert_error, valid_following_params, is_valid_id_int

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        following = Following.query.filter_by(user_id = self.current_user.id).all()
        following_data = [ follower.to_dict_following() for follower in following ]
        return Response(json.dumps(following_data), mimetype="application/json", status=200)

    
    @valid_following_params
    @handle_db_insert_error
    def post(self):
        body = request.get_json()
        following_id = body.get('user_id')
        user_id = self.current_user.id

        user = User.query.filter_by(id=following_id).all()
        if not user:
            return Response(json.dumps({'message': 'User does not exist'}), mimetype="application/json", status=404)

        following = Following(user_id, following_id)
        db.session.add(following)
        db.session.commit()

        return Response(json.dumps(following.to_dict_following()), mimetype="application/json", status=201)


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @is_valid_id_int
    def delete(self, id):
        following = Following.query.get(id)
        if not following or following.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Following does not exist'}), mimetype="application/json", status=404)
        Following.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Following {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
