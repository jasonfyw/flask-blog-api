from flask import Blueprint, jsonify, abort, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime 

from api.auth import auth
from api.mongodb_connection import posts, make_serialisable


comments = Blueprint('comments', __name__)

"""
API endpoints for interacting with comments
"""

# create new comment under post
@comments.route('/blog/comments/<string:post_id>', methods = ['POST'])
def create_comment(post_id):

    fields = ['name', 'email', 'text']
    if not request.json or any([not field in request.json for field in fields]):
        abort(400)

    comment = {
        '_id': ObjectId(),
        'name': request.json['name'],
        'email': request.json['email'],
        'text': request.json['text'],
        'parent_comment_id': ObjectId(request.json.get('parent_comment_id')) if request.json.get('parent_comment_id') else None,
        'timestamp': datetime.datetime.now()
    }

    result = posts.update_one(
        { '_id': ObjectId(post_id) },
        { 
            '$push': {
                'comments': comment
            }
        }
    )

    if not result.matched_count:
        abort(404)

    return jsonify(make_serialisable(comment))

# delete comment under post
@comments.route('/blog/comments/<string:post_id>/<string:comment_id>', methods = ['DELETE'])
@auth.login_required
def delete_comment(post_id, comment_id):
    result = posts.find_one_and_update(
        {'_id': ObjectId(post_id)},
        {
            '$pull': {
                'comments': {
                    '_id': ObjectId(comment_id)
                }
            }
        }
    )
    
    matched_comments = [comment for comment in result['comments'] if comment['_id'] == ObjectId(comment_id)]
    if not matched_comments:
        abort(404)

    return jsonify(make_serialisable(matched_comments[0]))