from flask import Blueprint, jsonify, abort, make_response, request
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import datetime

from auth import auth
from mongodb_connection import posts, make_serialisable


blogposts = Blueprint('blogposts', __name__)


"""
API endpoints
"""

# get all blogposts
@blogposts.route('/blog/posts', methods = ['GET'])
def get_all_posts():
    all_posts = list(posts.find())

    if len(all_posts) == 0:
        abort(404)

    for post in all_posts:
        post = make_serialisable(post)

    return jsonify({ "posts": all_posts })


# get blogpost by id
@blogposts.route('/blog/posts/<string:post_id>', methods = ['GET'])
def get_post(post_id):
    post = posts.find_one({ '_id': ObjectId(post_id) })

    if not post:
        abort(404)

    return jsonify(make_serialisable(post))


# create new blogpost
@blogposts.route('/blog/posts', methods = ['POST'])
@auth.login_required
def create_post():

    # validation, checks required fields
    fields = ['title', 'author', 'text']
    if not request.json or any([not field in request.json for field in fields]):
        abort(400)
    
    post = {
        'title': request.json['title'],
        'author': request.json['author'],
        'publishdate': datetime.datetime.now(),
        'category': request.json.get('category', ''),
        'text': request.json['text'],
        'visibility': True
    }

    # insert document into collection and return the blogpost
    post_id = posts.insert_one(post).inserted_id
    post['_id'] = str(post_id)

    return jsonify(post), 201


# update existing blogpost
@blogposts.route('/blog/posts/<string:post_id>', methods = ['PUT'])
@auth.login_required
def update_post(post_id):
    if not request.json:
        abort(400)
    
    fields = {'title': str, 'author': str, 'category': str, 'text': str, 'visibility': bool}
    updated_fields = {}
    for field in fields.keys():
        if field in request.json:
            # checks validity of data entry
            if type(request.json[field]) != fields[field]:
                abort(400)
            
            updated_fields[field] = request.json[field]

    # update and return updated document
    result = posts.find_one_and_update(
        { '_id': ObjectId(post_id) }, 
        { '$set': updated_fields },
        return_document=ReturnDocument.AFTER
    )

    if not result:
        abort(404)

    return jsonify(make_serialisable(result))

# delete existing blogpost
@blogposts.route('/blog/posts/<string:post_id>', methods = ['DELETE'])
@auth.login_required
def delete_post(post_id):
    # delete and return deleted document
    result = posts.find_one_and_delete({ '_id': ObjectId(post_id) })

    if not result:
        abort(404)

    return jsonify(make_serialisable(result))