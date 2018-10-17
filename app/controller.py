import bcrypt
import database
import pymongo
import datetime
from bson.json_util import dumps

# Global variables
db_con = database.get_db_conn()


def prepare():
    database.prepare_db()
    print("ASDASD")


def check_login_success(username, password):
    users = db_con.users
    login_user = users.find_one({'username': username})
    print('Trying loggin', username)
    if login_user:
        stored_password = login_user['password']
        # Comparing stored password and the users hashed password
        if bcrypt.hashpw(password.encode('utf8'),
                         stored_password) == stored_password:
            print('Login Success')
            return True
        else:
            print('Login Failed bad password')
            return False
    print('Login Failed user dont exist')
    return False


def check_register_success(username, password):
    print('Trying registering', username)
    users = db_con.users
    existing_user = users.find_one({'username': username})
    print('Trying registering', username)
    if existing_user is None:
        hashed = bcrypt.hashpw(password.encode('utf8'),
                               bcrypt.gensalt())  # Hashed pw
        print(hashed)
        users.insert(
            {'username': username, 'password': hashed})
        return True
    else:
        print('Register Failed')
        return False

def add_story(content):
    print('Trying to add story to DB', content['title'])
    story = format_story(content)
    items = db_con.items
    if items.insert(story):
        print('Added', story['id'])
        return story
    else:
        print('Can\'t add story')
        return False


def get_all_items():
    print('Trying getting all items')
    items = db_con.items
    itemList = items.find({'type': 'story'})
    return itemList


def get_item_by_id(id):
    print('Trying getting one item by ID')
    items = db_con.items
    itemList = items.find_one({"id": id})
    return itemList


def delete_item_by_id(id):
    print('Trying delete item by ID')
    items = db_con.items
    item = items.find_one({"id":id})
    if item:
        items.update_one({"id": id},
            {'$set': {'deleted': True}}, upsert=False)
        return True
    else:
        return False

def insert_post(post):
    posts = db_con.posts
    if posts.insert(post):
        print('Post inserted')
        return post
    else:
        print("Can't add post")
        return None

def latest_post():
    posts = db_con.posts
    post = posts.find_one({}, {'_id': False}, sort=[('added', pymongo.DESCENDING)])
    print(post)
    return post

# helper methods
def format_story(content):
    content['id'] = len(dumps(get_all_items()))
    content['descendants'] = 7 #just a number, not sure about This
    content['kids'] = []
    content['score'] = 123 #just a number, not sure about This
    content['time'] = datetime.datetime.today()
    content['type'] = 'story'
    content['deleted'] = False
    content['poll'] = 222
    content['parts'] = []
    return content
