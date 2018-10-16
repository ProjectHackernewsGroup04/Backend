import bcrypt
import database
import datetime
import pymongo
from bson.json_util import dumps

# Global variables
db_con = database.get_db_conn()

# Checking if login success by looking up the database
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


# Checking if registering success by looking up the database
# If username already exist, it will return False
# If username dont exist, it will insert a new user 
# - with a hashed password in database using bcrypt algorithm
def check_register_success(username, password):
    print('Trying registering', username)
    users = db_con.users
    existing_user = users.find_one({'username': username})
    print('Trying registering', username)
    if existing_user is None:
        hashed = bcrypt.hashpw(password.encode('utf8'),
                               bcrypt.gensalt())  ## Hashed pw
        print(hashed)
        users.insert(
            {'username': username, 'password': hashed})
        return True
    else:
        print('Register Failed')
        return False

# Inserting a item(story) into the database
def add_story(content):
    print('Trying to add story to DB', content['title'])
    story = format_story(content)
    items = db_con.items
    if items.insert(story):
        return True
    else:
        print('Can\'t add story')
        return False

# Getting all items from database
def get_all_items():
    print('Trying getting all items')
    items = db_con.items
    itemList = items.find({'type': 'story'})
    return itemList

# Getting a single item by id
def get_item_by_id(id):
    print('Trying getting one item by ID')
    items = db_con.items
    itemList = items.find_one({"id": id})
    return itemList

# Set the property "deleted" to True for the item by id
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


# helper formatting methods
# Notice that the id will be incremented by len of all items
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

# Getting the latest created object in mongodb using timestamp function in objectid
def get_latest_id():
    items = db_con.items
    item = items.find_one(sort=[('_id', pymongo.DESCENDING)])
    return int(item["id"])

# HelgeAPI
# Getting the latest created object in mongodb using timestamp function in objectid
def get_latest_post_id():
    posts = db_con.posts
    item = posts.find_one(sort=[('_id', pymongo.DESCENDING)])
    return int(item["hanesst_id"])

# HelgeApi
# Formatting and inserting the message from rabbit into database
def add_post(message):
    posts = db_con.posts
    data = json.loads(message)
    posts.insert_one(data)
    print("object inserted")