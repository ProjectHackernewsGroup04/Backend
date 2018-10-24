from flask import Flask, url_for, request, session, redirect, jsonify
from flask_httpauth import HTTPBasicAuth
from bson.json_util import dumps
from threading import Thread
import time
import sys
import controller

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'hackernews'
auth = HTTPBasicAuth()
thread = None


@auth.verify_password
def verify_password(username, password):
    return controller.check_login_success(username, password)


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
    if controller.check_login_success(username, password):
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
    if controller.check_register_success(username, password):
        app.logger.info('Register Success')
        return jsonify({'statusCode': 200,
                        'message': 'User created successed'}), 200
    else:
        app.logger.info('Register failed')
        return jsonify({'statusCode': 400,
                        'errorMessage': 'User already registered'}), 400


# Logout
@app.route('/api/logout', methods=['GET'])
@auth.login_required
def api_logout():
    return {}


# Add story
@app.route('/api/submit', methods=['POST'])
# @auth.login_required
def api_add_story():
    content = request.json
    app.logger.info('Adding a story')
    story = controller.add_story(content)
    if story:
        app.logger.info('Story Successfully Added')
        return dumps({'statusCode': 200,
                        'story': story}), 200
    else:
        app.logger.info('Add Story Failed')
        return dumps({'statusCode': 400,
                        'errorMessage': 'Adding Story Failed.'}), 400


# Edit story
@app.route('/api/edit<int:id>', methods=["POST"])
@auth.login_required
def api_edit_story():
    return {}


# Get all stories
@app.route('/api/item/all', methods=['GET'])
def api_all():
    app.logger.info('Getting all items')
    cursor = controller.get_all_items()
    return dumps({'statusCode': 200, 'items': cursor}), 200


# Get item by id
@app.route('/api/item/<int:id>', methods=['GET'])
def api_get_item_by_id(id):
    app.logger.info('Getting all items by ID')
    cursor = controller.get_item_by_id(id)
    return dumps({'statusCode': 200, 'item': cursor}), 200


# Delete item by id
@app.route('/api/item/<int:id>', methods=['DELETE'])
@auth.login_required
def api_delete_item_by_id(id):
    app.logger.info('Getting all items by ID')
    if controller.delete_item_by_id(id):
        return jsonify({'statusCode': 200,
                        'message': 'Item deleted'}), 200

    else:
        return jsonify({'statusCode': 400,
                        'errorMessage': 'Item doesnt exist, not deleted'}), 400


# Add Comment
@app.route('/api/comment', methods=['POST'])
# @auth.login_required
def api_add_comment():
    content = request.json
    app.logger.info('Adding a comment')
    result = controller.add_comment(content)
    if result:
        app.logger.info('Story Successfully Updated with Comment')
        return dumps({'statusCode': 200,
                        'story': result}), 200
    else:
        app.logger.info('Add Comment Failed')
        return dumps({'statusCode': 400,
                        'errorMessage': 'Adding Comment Failed.'}), 400



@app.route('/latest', methods=['GET'])
def latest_digested():
    # Integration to DB
    post = controller.latest_post()
    return jsonify({'statusCode': 200, 'post': post}), 200


@app.route('/status', methods=['GET'])
def status():
    status = {'status': 'Alive'}
    return jsonify(status), 200


@app.route('/webhook', methods=['POST'])
def webhook():
    post = request.json
    print(post, file=sys.stderr)
    return jsonify({"status": "success"}), 200
    # return jsonify(controller.insert_post(post)), 200


# Run the app on 0.0.0.0:5000
if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        CSRF_ENABLED=True,
    )
    controller.prepare()
    app.run(debug=True, host='0.0.0.0')
