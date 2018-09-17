from flask import Flask
from bson.json_util import dumps

# API DOCUMENTATION : https://github.com/HackerNews/API
# Python API service running on Flask framework,
# connected to a mongodb database.

# Local functions
from database import (
    get_db_conn,
    prepare_db,
    collection_name_items,
)

# Global variables
db_connection = None
app = Flask(__name__)


# Temporally homepage
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# Get all stories
@app.route('/api/v1/item/all', methods=['GET'])
def api_all():
    db_con = get_db_conn()
    col = db_con[collection_name_items]
    cursor = col.find({})
    return dumps(cursor)


# Get item by id
@app.route('/api/v1/item/<int:post_id>', methods=['GET'])
def api_get_item_by_id(post_id):
    col = db_connection[collection_name_items]
    cursor = col.find({"id": post_id})
    return dumps(cursor)


@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def api_get_user_by_id(user_id):
    # show the post with the given id, the id is an integer
    return 'User %d' % user_id


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# Run the app on 0.0.0.0:5000
if __name__ == '__main__':
    prepare_db()
    app.run(debug=True, host='0.0.0.0')
