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
    cursor = controller.get_all_items()
    return dumps(cursor), 200


# Get item by id
@app.route('/api/item/<int:id>', methods=['GET'])
def api_get_item_by_id(id):
    app.logger.info('Getting all items by ID')
    cursor = controller.get_item_by_id(id)
    return dumps({'statusCode': 200, 'item': cursor}), 200


# Delete item by id
@app.route('/api/item/<int:id>', methods=['DELETE'])
def api_delete_item_by_id(id):
    app.logger.info('Getting all items by ID')
    if controller.delete_item_by_id(id):
        return jsonify({'statusCode': 200,
                        'message': 'Item deleted'}), 200

    else:
        return jsonify({'statusCode': 400,
                        'errorMessage': 'Item doesnt exist, not deleted'}), 400



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
