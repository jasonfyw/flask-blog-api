from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv


"""
MongoDB setup
"""
# load MongoDB details from .env file
load_dotenv(find_dotenv())
MONGODB_URI = os.environ.get('MONGODB_URI')
DB_NAME = os.environ.get('DB_NAME')

# create MongoDB client, connect to posts collection in given db
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
posts = db.posts


"""
Make post JSON serialisable
"""

# convert _id field in a document from ObjectId into a serialisable string
def make_serialisable(post):
    post['_id'] = str(post['_id'])
    if 'comments' in post.keys():
        for comment in post['comments']:
            comment['_id'] = str(comment['_id'])
    return post