import flask
from flask import request, jsonify
import pymongo

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def getConn():
    myclient = pymongo.MongoClient('localhost', 27017)
    dblist = myclient.list_database_names()
    if "mydatabase" in dblist:
        print("The database exists.")
        mydb = myclient["mydatabase"]
    return mydb


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/item/all', methods=['GET'])
def api_all():
   return 'asd'

@app.route('/api/v1/item/<int:post_id>', methods=['GET'])
def api_getItemByID(post_id):
    # show the post with the given id, the id is an integer
    return 'Item %d' % post_id

@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def api_getUserByID(user_id):
    # show the post with the given id, the id is an integer
    return 'User %d' % user_id

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run()