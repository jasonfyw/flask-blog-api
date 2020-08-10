from flask import Flask, jsonify, abort, make_response, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime

app = Flask(__name__)

"""
MongoDB setup
"""
# load MongoDB details from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
MONGODB_URI = os.environ.get('MONGODB_URI')
DB_NAME = os.environ.get('DB_NAME')

# create MongoDB client, connect to posts collection in given db
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
posts = db.posts

def make_serialisable(post):
    post['_id'] = str(post['_id'])
    return post


"""
API endpoints
"""

# get all posts
@app.route('/blog/posts', methods = ['GET'])
def get_all_posts():
    all_posts = list(posts.find())

    if len(all_posts) == 0:
        abort(404)

    for post in all_posts:
        post = make_serialisable(post)

    return jsonify({ "posts": all_posts })

# get post by id
@app.route('/blog/posts/<string:post_id>', methods = ['GET'])
def get_post(post_id):
    print(post_id)
    post = posts.find_one({ '_id': ObjectId(post_id) })

    if not post:
        abort(404)

    return jsonify(make_serialisable(post))

@app.route('/blog/posts', methods = ['POST'])
def create_post():
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

    post_id = posts.insert_one(post).inserted_id
    post['_id'] = str(post_id)

    return jsonify({'post': post}), 201


"""
Error handling
"""
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({ 'error': 'Not found' }), 404)


if __name__ == "__main__":
    app.run(debug = True)



'''
DB:

_id
title
author
publishdate
category
text
visibility
'''