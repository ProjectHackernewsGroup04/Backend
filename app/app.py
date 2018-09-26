from flask import Flask, url_for, request, session, redirect, jsonify
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
def api_home():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return redirect(url_for('/'))


# Login
@app.route('/api/login', methods=['POST'])
def api_login():
    users = db_con.users
    content = request.json
    username = content['username']
    password = content['password']
    login_user = users.find_one({'username': username})
    app.logger.info('Trying loggin')
    app.logger.info(username)
    if login_user:
        if password == login_user['password']:
            app.logger.info('Login Success')

            return jsonify({'statusCode': 200,
                            'message': 'Login Success'}), 200
    app.logger.info('Login Failed')
    return jsonify({'statusCode': 400, 'errorMessage': 'Bad Login'}), 400


# Register
@app.route('/api/register', methods=['POST'])
def api_register():
    users = db_con.users
    content = request.json
    username = content['username']
    password = content['password']
    existing_user = users.find_one({'username': username})
    if existing_user is None:
        hash_psw = password  # adding hash later
        users.insert(
            {'username': username, 'password': hash_psw})
        return jsonify({'statusCode': 200, 'message': 'User created successed'}), 200
    else:
        return jsonify('That username already exists!'), 400


# Logout
@app.route('/api/logout', methods=['GET'])
def api_logout():
    return {}


# Add story
@app.route('/api/submit', methods=['POST'])
def api_add_story():
    return {}


# Edit story
@app.route('/api/edit<int:id>', methods=["POST"])
def api_edit_story():
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
