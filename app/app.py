from flask import Flask, url_for, request, session, redirect
from bson.json_util import dumps

# Database imports
from database import (
    collection_name_items,
    get_db_conn,
    prepare_db,
)

app = Flask(__name__)

# Global variables
db_con = get_db_conn()
app.config['MONGO_DBNAME'] = 'hackernews'


@app.route('/')
def home():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return redirect(url_for('/'))


# Login
@app.route('/login', methods=['POST'])
def login():
    users = db_con.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if (request.form['password'].encode('utf-8'), login_user['password']
                .encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']

            return redirect(url_for('home')), 200

    return 'Invalid username/password', 400


# # Register
# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         users = db_con.db.users
#         existing_user = users.find_one({'name': request.form['username']})
#
#         if existing_user is None:
#             hash_psw = (request.form['password'].encode('utf-8'))
#             users.insert(
#                 {'name': request.form['username'], 'password': hash_psw})
#             session['username'] = request.form['username']
#             return redirect(url_for('/'))
#
#         return 'That username already exists!'
#
#     return redirect(url_for('/'))


# Logout
@app.route('/api/logout', methods=['GET'])
def logout():
    return {}


# Add story
@app.route('/api/submit', methods=['POST'])
def add_story():
    return {}


# Get all stories
@app.route('/api/item/all', methods=['GET'])
def api_all():
    col = db_con[collection_name_items]
    cursor = col.find({})
    return dumps(cursor)


# Get item by id
@app.route('/api/item/<int:post_id>', methods=['GET'])
def api_get_item_by_id(post_id):
    col = db_con[collection_name_items]
    cursor = col.find({"id": post_id})
    return dumps(cursor)


@app.route('/api/user/<int:user_id>', methods=['GET'])
def api_get_user_by_id(user_id):
    # show the post with the given id, the id is an integer
    return 'User %d' % user_id


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# Run the app on 0.0.0.0:5000
if __name__ == '__main__':
    prepare_db()
    app.config.update(
        DEBUG=True,
        CSRF_ENABLED=True,
    )
    app.run(debug=True, host='0.0.0.0')
