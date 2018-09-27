from flask import Flask, url_for, request, session, redirect, jsonify
from bson.json_util import dumps
import controller

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'hackernews'


@app.route('/')
def api_home():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return redirect(url_for('/'))


# Login
@app.route('/api/login', methods=['POST'])
def api_login():
    content = request.json
    username = content['username']
    password = content['password']
    app.logger.info('Trying Login')
    if controller.checkIfloginSuccess(username, password):
        app.logger.info('Login Success')
        return jsonify({'statusCode': 200,
                        'message': 'Login Success'}), 200
    else:
        app.logger.info('Login Failed')
        return jsonify({'statusCode': 400, 'errorMessage': 'Bad Login'}), 400


# Register
@app.route('/api/register', methods=['POST'])
def api_register():
    content = request.json
    username = content['username']
    password = content['password']
    app.logger.info('Trying Registering')
    if controller.checkIfRegisterSuccess(username, password):
        app.logger.info('Register Success')
        return jsonify({'statusCode': 200,
                        'message': 'User created successed'}), 200
    else:
        app.logger.info('Register failed')
        return jsonify({'statusCode': 400,
                        'errorMessage': 'User already registered'}), 400


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
    app.logger.info('Getting all items')
    cursor = controller.getAllItems()
    return dumps(cursor), 200


# Get item by id
@app.route('/api/item/<string:post_id>', methods=['GET'])
def api_get_item_by_id(post_id):
    app.logger.info('Getting all items by ID')
    cursor = controller.getItemsByID(post_id)
    return dumps(cursor), 200


# Delete item by id
# @app.route('/api/item/<int:post_id>', methods=['GET'])
# def api_get_item_by_id(post_id):
#     col = db_con[collection_name_items]
#     cursor = col.find({"id": post_id})
#     return dumps(cursor)


@app.route('/api/user/<int:user_id>', methods=['GET'])
def api_get_user_by_id(user_id):
    # show the post with the given id, the id is an integer
    return 'User %d' % user_id


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# Run the app on 0.0.0.0:5000
if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        CSRF_ENABLED=True,
    )
    controller.prepare()
    app.run(debug=True, host='0.0.0.0')
