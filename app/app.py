from flask import Flask, url_for, request, session, redirect, jsonify, Response
from flask_httpauth import HTTPBasicAuth
from bson.json_util import dumps
from threading import Thread
import time
import sys
import controller
from log import log_handler as log

from prometheus_client import start_http_server, Summary, Counter, Gauge, generate_latest, REGISTRY, Histogram

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# A counter to count the total number of HTTP requests
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests (count)', ['method', 'endpoint', 'status_code'])

# A gauge (i.e. goes up and down) to monitor the total number of in progress requests
IN_PROGRESS = Gauge('http_requests_inprogress', 'Number of in progress HTTP requests')

# A histogram to measure the latency of the HTTP requests
TIMINGS = Histogram('http_request_duration_seconds', 'HTTP request latency (seconds)')


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
        log.log_info("API: Login attemt successed") 
        return jsonify({'statusCode': 200,
                        'message': 'Login Success'}), 200
    else:
        app.logger.info('Login Failed')
        log.log_info("API: Login attemt failed") 
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
        log.log_info("API: User registation success") 
        return jsonify({'statusCode': 200,
                        'message': 'User created successed'}), 200
    else:
        app.logger.info('Register failed')
        log.log_info("API: User registation failed") 
        return jsonify({'statusCode': 400,
                        'errorMessage': 'User already registered'}), 400


# Logout
@app.route('/api/logout', methods=['GET'])
@auth.login_required
def api_logout():
    return {}


# Add story
@app.route('/api/submit', methods=['POST'])
@IN_PROGRESS.track_inprogress()
@TIMINGS.time()
def api_add_story():
    REQUESTS.labels(method='POST', endpoint="/api/submit", status_code=200).inc()
    content = request.json
    story = controller.add_story(content)
    if story:
        return dumps({'statusCode': 200,
                        'story': story}), 200
    else:
        return dumps({'statusCode': 400,
                        'errorMessage': 'Adding Story Failed.'}), 400



# Edit story
@app.route('/api/edit/<string:id>', methods=["PUT"])
#@auth.login_required
def api_edit_item_by(id):
    content = request.json
    app.logger.info('Getting all items by ID')
    if controller.edit_item_by(content):
        return jsonify({'statusCode': 200,
                        'message': 'Item edited'}), 200

    else:
        return jsonify({'statusCode': 400,
                        'errorMessage': 'Item doesnt exist, not edited'}), 400


# Get all stories
@app.route('/api/item/all', methods=['GET'])
def api_all():
    app.logger.info('Getting all items')
    cursor = controller.get_all_items()
    log.log_info("API: Getting all items") 
    return dumps({'statusCode': 200, 'items': cursor}), 200

# Get chunked stories FROM row number -> TO row number
@app.route('/api/item/pagination/', methods=['GET'])
def api_all_limited():
    row_from = request.args.get('from')
    row_to = request.args.get('to')
    app.logger.info('Getting items from',row_from, 'to',row_to)
    cursor = controller.get_all_items_limited(row_from,row_to)
    return dumps({'statusCode': 200, 'items': cursor}), 200



# Get item by id
@app.route('/api/item/<string:id>', methods=['GET'])
def api_get_item_by_id(id):
    app.logger.info('Getting all items by ID')
    cursor = controller.get_item_by_id(id)
    return dumps({'statusCode': 200, 'item': cursor}), 200


# Delete item by id
@app.route('/api/item/<string:id>', methods=['DELETE'])
@auth.login_required
def api_delete_item_by_id(id):
    app.logger.info('Delete item by id')
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
        log.log_info("API: Story Successfully Updated with Comment") 
        return dumps({'statusCode': 200,
                        'story': result}), 200
    else:
        app.logger.info('Add Comment Failed')
        log.log_info("API Story Failed Updated with Comment") 
        return dumps({'statusCode': 400,
                        'errorMessage': 'Adding Comment Failed.'}), 400


@app.route('/latest', methods=['GET'])
def latest_digested():
    # Integration to DB hehe
    post = controller.latest_post()
    return jsonify({'statusCode': 200, 'post': post}), 200


@app.route('/status', methods=['GET'])
def status():
    status = {'status': 'Alive'}
    return jsonify(status), 200


@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request,flush=True)
    post = request.json
    #print(post,flush=True)
    return jsonify(controller.insert_post(post)), 200

@app.errorhandler(500)
def handle_500(error):
    return str(error), 500


@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(REGISTRY)

# Run the app on 0.0.0.0:5000
if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        CSRF_ENABLED=True,
    )
    controller.prepare()
    app.run(debug=True, host='0.0.0.0')
