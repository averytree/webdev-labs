from flask import Response
from flask_restful import Resource
from models import LikePost, db, Post
import json
from . import can_view_post
from my_decorators import is_valid_id_int, handle_db_insert_error, secure_post, is_valid_like_post_id, is_valid_int_2x

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @handle_db_insert_error
    def post(self, post_id):
        print(post_id)
        try:
            post_id = int(post_id)
        except:
            response_obj = {
                'message': 'Invalid post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        
        post = Post.query.get(post_id)
        if post and can_view_post(post.id, self.current_user):
            user_id = self.current_user.id
            like = LikePost(user_id, post.id)
            db.session.add(like)
            db.session.commit()
            return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)
        else:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
             

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, post_id, id):
        try:
            post_id = int(post_id)
            id = int(id)
        except:
            response_obj = {
                'message': 'Invalid id or post id'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        like = LikePost.query.get(id)
        if not like or like.user_id != self.current_user.id or like.post_id != post_id:
            return Response(json.dumps({'message': 'Like does not exist'}), mimetype="application/json", status=404)
        LikePost.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
             'message': 'Like {0} successfully deleted.'.format(id)
         }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )

