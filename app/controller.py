import bcrypt
import database
import pymongo
import datetime
import json
from bson.json_util import dumps
import base64
import sys
import uuid

# Global variables
db_con = database.get_db_conn()

def prepare():
    database.prepare_db()


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
    users = db_con.users
    print('Trying registering', username)
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
    items = db_con.items
    print('Trying to add story to DB', content['title'])
    story = format_story(content)
    if items.insert(story):
        print('Added', story['id'])
        return story
    else:
        print('Can\'t add story')
        return False


def get_all_items():
    items = db_con.items
    print('Trying getting all items')
    itemList = items.find({'type': 'story'}, sort=[('_id', pymongo.DESCENDING)])
    return itemList

def get_all_items_limited(row_from,row_to):
    items = db_con.items
    print('Trying getting limited items')
    itemList = items.find({'type': 'story'}, sort=[('_id', pymongo.DESCENDING)]).skip(int(row_from)).limit(int(row_to))
    return itemList


def get_item_by_id(id):
    print('Trying getting one item by ID')
    story = construct_story(id)
    return story


def delete_item_by_id(id):
    items = db_con.items
    print('Trying delete item by ID')
    item = items.find_one({"id":id})
    if item:
        items.update_one({"id": id},
            {'$set': {'deleted': True}}, upsert=False)
        return True
    else:
        return False

def add_comment(content):
    items = db_con.items
    print('Trying to add comment to DB on ', content['by'])
    comment = format_comment(content)
    if items.insert(comment):
        print('Added', comment['id'])
        #update parent
        story = add_comment_to_parent(content['parent'], comment['id'])
        if story is not None:
            return story
        else:
            return False
    else:
        print('Adding a comment failed')
        return False

def add_comment_to_parent(parent, child):
    items = db_con.items
    if items.update({"id": parent},
        {'$push': { "kids": child }}):
        return construct_story(parent)
    else:
        return False

def insert_post(post):
    username_password = decode_basic_auth(post['auth'])
    username = username_password[0]
    password = username_password[1]
    if not check_login_success(username, password):
        check_register_success(username, password)

    items = db_con.items

    if post['post_type'] == 'story':
        item = {
            'id': str(post['hanesst_id']),
            'descendants': 0,
            'kids': [],
            'score': 0,
            'time': datetime.datetime.now(),
            'type': 'story',
            'deleted': False,
            'poll': False,
            'parts': [],
            'parent': -1,
            'text': post['post_text'],
            'url': post['post_url'],
            'title': post['post_title'],
            'by': username,
            'hanesst_id': post['hanesst_id']
        }
        if items.insert(item):
            item.pop('_id', None)
            update_hanesst(item)
            return item

    if post['post_type'] == 'comment':
        item = {
            'id': str(post['hanesst_id']),
            'descendants': 0,
            'kids': [],
            'score': 0,
            'time': datetime.datetime.now(),
            'type': 'comment',
            'deleted': False,
            'poll': False,
            'parts': [],
            'parent': str(post['post_parent']),
            'text': post['post_text'],
            'url': '',
            'title': '',
            'by': username,
            'hanesst_id': post['hanesst_id']
        }
        if items.insert(item):
            add_comment_to_parent(str(post['post_parent']), item['id'])
            item.pop('_id', None)
            update_hanesst(item)
            return item

    print("Can't add post")
    return post


def update_hanesst(item):
    hanesst = db_con.hanesst

    latest = hanesst.find_one({})
    print(latest, flush=True)
    if not latest:
        hanesst.insert(item)
    elif latest['hanesst_id'] < item['hanesst_id']:
        hanesst.update_one({"hanesst_id": latest['hanesst_id']},
                           {'$set': {'hanesst_id': item['hanesst_id']}}, upsert=False)


def latest_post():
    hanesst = db_con.hanesst

    latest = hanesst.find_one({}, {'_id': False})

    if latest:
        return latest
    else:
        items = db_con.items
        item = items.find_one({}, {'_id': False}, sort=[('time', pymongo.DESCENDING)])
        return item


def edit_item_by(content):
    print('Trying editin item by ID', content['url'])
    items = db_con.items
    item = items.find_one({"id": content['id']})
    if item:
        items.update_one({"id": content['id']},
            {'$set': {'url': content['url'] ,'title': content['title']}}, upsert=False)
        return True
    else:
        return False


# helper methods
def format_story(content):
    items = db_con.items
    content['id'] = uuid.uuid4().hex
    content['descendants'] = 7 #just a number, not sure about This
    content['kids'] = []
    content['score'] = 3
    content['time'] = datetime.datetime.now()
    content['type'] = 'story'
    content['deleted'] = False
    content['poll'] = 222
    content['parts'] = []
    content['parent'] = -1
    return content

def format_comment(content):
    items = db_con.items
    content['id'] = uuid.uuid4().hex
    content['descendants'] = 7 #just a number, not sure about This
    content['kids'] = []
    content['score'] = 1
    content['time'] = datetime.datetime.now()
    content['type'] = 'comment'
    content['deleted'] = False
    content['poll'] = 222
    content['parts'] = []
    content['title'] = ''
    content['url'] = ''
    return content

def construct_story(id):
    items = db_con.items
    story = items.find_one({"id":id}, sort=[('kids', pymongo.DESCENDING)])
    print(story, file=sys.stderr)
    print(id, file=sys.stderr)
    if story is not None:
        story['by'] = get_user(story['by'])
        story['kids'] = get_comments(story['id'])
        return story
    else:
        return None

def get_user(username):
    users = db_con.users
    return users.find_one({"username": username})

def get_comments(parent):
    items = db_con.items
    comments = list(items.find({"parent": parent}))
    arr = []
    for comment in comments:
        if not comment['kids']: # If no kids
            arr.append(comment)
        else: # If have kids going recursive
            kids = comment['kids'] # Array of kids id
            comment['kids'] = []
            for kid in kids:
                nested_arr = []
                comment_id = comment['id']
                nested_list = get_nested_children(nested_arr,comment_id)
                for item in nested_list:
                    if item not in comment['kids']:
                        comment['kids'].append(item)
            arr.append(comment)
    return arr

def get_nested_children(arr,parent):
    items = db_con.items
    comments = list(items.find({"parent": parent}))
    for comment in comments:
        if not comment['kids']: # If no kids
            arr.append(comment)
        else: # If have kids going recursive
            kids = comment['kids'] # Array of kids id
            comment['kids'] = []
            for kid in kids:
                nested_arr = []
                comment_id = comment['id']
                nested_list = get_nested_children(nested_arr,comment_id)
                for item in nested_list:
                    if item not in comment['kids']:
                        comment['kids'].append(item)
            arr.append(comment)
    return arr

def decode_basic_auth(auth):
    b64string = auth[8:-1]
    b = base64.b64decode(b64string)
    b_string = b.decode('utf-8')
    return b_string.split(':')

