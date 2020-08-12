from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv


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

# convert _id field in a document from ObjectId into a serialisable string
def make_serialisable(post):
    post['_id'] = str(post['_id'])
    return post