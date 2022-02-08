from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json
from . import can_view_post
from my_decorators import handle_db_insert_error,secure_bookmark, check_ownership_of_bookmark, is_valid_post_id_int, is_valid_id_int

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).order_by('id').all()
        bookmark_list_of_dict = [
            bookmark.to_dict() for bookmark in bookmarks
        ]
        return Response(json.dumps(bookmark_list_of_dict), mimetype="application/json", status=200)

    @is_valid_post_id_int
    @secure_bookmark
    @handle_db_insert_error
    def post(self):
        '''
        1. get post_id from request body
        2. check that the user is authorized to bookmark the post
        3. check that the post_id exists and is valid
        4. insert into database
        5. return new bookmarked post (and bookmark id) to the user as part of the response
        '''
        body = request.get_json() #data that user sent us
        post_id = body.get('post_id')


        bookmark = Bookmark(self.current_user.id, post_id)
        db.session.add(bookmark)
        db.session.commit()
       
        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @is_valid_id_int
    def delete(self, id):
        # Your code here
        bookmark = Bookmark.query.get(id)
        if not bookmark or bookmark.user_id != self.current_user.id:
             return Response(json.dumps({'message': 'Bookmark does not exist'}), mimetype="application/json", status=404)
        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Bookmark {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<id>', 
        '/api/bookmarks/<id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
