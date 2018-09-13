import flask
from flask import request, jsonify
from pymongo import MongoClient
import os
import json
from bson.json_util import dumps


# API DOCUMENTATION : https://github.com/HackerNews/API
# This is a python API service running on Flask framework.
# Connected to a mongodb database.


# Various database names
databaseName = "hackernews"
collectionNameItems = "items"
collectionNameUsers = "users"
sampleData = {"id":1,"by":"TestUser","type":"story"}

# Global variables
dbCon = None
app = flask.Flask(__name__)

def getDBConnection():
    myclient = MongoClient('db',
    27017)
    print(myclient.list_database_names())
    connection = myclient[databaseName]
    return connection

def prepareDatabase():
    dbCon = getDBConnection()
    col = dbCon[collectionNameItems]
    # Checking if the collection is empty
    if col.count() == 0:
        print("Database is empty, adding sample data")
        col.insert_one(sampleData)
        print("Sampledata added in database")
    print("Connection to DB successed")

# Temporaily homepage
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

# Get all stories
@app.route('/api/v1/item/all', methods=['GET'])
def api_all():
   dbCon = getDBConnection()
   col = dbCon[collectionNameItems]
   cursor = col.find({})
   return dumps(cursor)

# Get item by ID
@app.route('/api/v1/item/<int:post_id>', methods=['GET'])
def api_getItemByID(post_id):
   col = dbCon[collectionNameItems]
   cursor = col.find({"id":post_id})
   return dumps(cursor)


@app.route('/api/v1/user/<int:user_id>', methods=['GET'])
def api_getUserByID(user_id):
    # show the post with the given id, the id is an integer
    return 'User %d' % user_id

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# Run the app on 0.0.0.0:5000
if __name__ == '__main__':
    prepareDatabase()
    app.run(debug=True,host='0.0.0.0')