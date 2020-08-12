from flask import Flask, jsonify, make_response

from blogposts import blogposts
from auth import token
from comments import comments

app = Flask(__name__)


"""
Error handling
"""
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({ 'error': 'Not found' }), 404)


"""
Register blueprints to app
"""
app.register_blueprint(blogposts)
app.register_blueprint(token)
app.register_blueprint(comments)


if __name__ == "__main__":
    app.run(debug = True)
