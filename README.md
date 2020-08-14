# flask-blog-api
A simple RESTful blogging API built with Flask and MongoDB! It has support for simple comments under posts and protected endpoints for the admin to manage posts.

It's easy to get it up and running and can be hooked up to a frontend without too much trouble!

## Installation

To run the API locally, navigate to your desired directory and clone the repository:

```
$ git clone https://github.com/jasonfyw/flask-blog-api
```

Then, ensure you have all the dependencies installed, and you're ready to start setting the blog!

```
$ cd flask-blog-api
$ pip install -r requirements.txt
```

## Setup

Create a `.env` file and enter in the following fields:

* `MONGODB_URI`: the URI of the MongoDB instance the blog will live in
* `DB_NAME`: the name of the database the blog will live in
* `ADMIN_PASSWORD`: the password for the admin login (yes, in plain text, fight me)
* `SECRET_KEY`: a random string to act as the secret key (will be used to generate authentication tokens)

## Usage

Once you have everything set up, you can try the API out!

To start the Flask app, run:

```
$ python run.py
```

The app should now be running on `localhost:5000`

Now, using curl or whatever client you want (Insomnia, Postman),  you can interact with the API! The currently available endpoints are detailed in the table below (a note on authentication follows).

### Endpoints

| Endpoint                                | Method   | Protected? | Description                                                                                                                                            | Returns         |
|-----------------------------------------|----------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| `/blog/posts`                           | `GET`    | No         | Returns all posts (includes all details and comments                                                                                                   | Array of posts  |
| `/blog/posts/<post_id>`                 | `GET`    | No         | Returns a single post (and subsidiary comments) matching provided `post_id`                                                                            | Retrieved post  |
| `/blog/posts`                           | `POST`   | Yes        | Create a new post (entry fields: `title`, `author`, `text`, `category` – *the last field is optional*)                                                 | Created post    |
| `/blog/posts/<post_id>`                 | `PUT`    | Yes        | Update an existing post (updateable fields: `title`, `author`, `text`, `category`, `visibility`)                                                       | Edited post     |
| `/blog/posts/<post_id>`                 | `DELETE` | Yes        | Deletes an existing post by `post_id`                                                                                                                  | Deleted post    |
| `/blog/comments/<post_id>`              | `POST`   | No         | Create a new comment under a post identified by `post_id` (entry fields: `name`, `email`, `text`, `parent_comment_id` – *the last field is optional*)  | Created comment |
| `/blog/comments/<post_id>/<comment_id>` | `DELETE` | Yes        | Deleted a comment under post identified by `post_id` with id `comment_id`                                                                              | Deleted comment |
| `/auth/token`                           | `GET`    | Yes        | Returns a temporary token to use instead of login credentials                                                                                          | Token string    |


### Authentication and tokens

For protected endpoints, this API uses Basic authentication. Pass in the username and password with the API call to access these endpoints.

Alternatively, for convenience, use the username/password once to generate a token from endpoint `/auth/token`, which you can pass as the username in following requests instead (password field is ignored in this case).

## Deployment

For production, deploy this Flask app to your provider of choice and you can make calls to it from your frontend client to produce a beautiful, end-product blog.