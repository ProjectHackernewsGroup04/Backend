import bcrypt
import database
import pymongo
import datetime
from bson.json_util import dumps

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
    itemList = items.find({'type': 'story'}, sort=[('id', pymongo.ASCENDING)])
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
    content['parent'] = int(content['parent'])
    comment = format_comment(content)
    if items.insert(comment):
        print('Added', comment['id'])
        #update parent
        story = add_comment_to_parent(content['parent'], comment['id'])
        return story
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
    username = post['username']
    password = post['pwd_hash']
    if not check_login_success(username, password):
        check_register_success(username, password)

    items = db_con.items

    if post['post_type'] == 'story':
        item = {
            'id': items.count,
            'descendants': 0,
            'kids': [],
            'score': 0,
            'time': datetime.datetime.today(),
            'type': 'story',
            'deleted': False,
            'poll': False,
            'parts': [],
            'parent': -1,
            'text': post['post_text'],
            'url': post['post_url'],
            'title': post['title'],
            'by': post['username'],
            'harnesst_id': post['harnesst_id']
        }
        if items.insert(item):
            return item

    if post['post_type'] == 'comment':
        item = {
            'id': items.count,
            'descendants': 0,
            'kids': [],
            'score': 0,
            'time': datetime.datetime.today(),
            'type': 'comment',
            'deleted': False,
            'poll': False,
            'parts': [],
            'parent': post['post_parent'],
            'text': post['post_text'],
            'url': '',
            'title': '',
            'by': post['username'],
            'harnesst_id': post['harnesst_id']
        }
        if items.insert(item):
            add_comment_to_parent(post['post_parent'], item['id'])
            return item

    print("Can't add post")
    return None

def latest_post():
    posts = db_con.posts
    post = posts.find_one({}, {'_id': False}, sort=[('added', pymongo.DESCENDING)])
    print(post)
    return post

# helper methods
def format_story(content):
    items = db_con.items
    content['id'] = items.count()
    content['descendants'] = 7 #just a number, not sure about This
    content['kids'] = []
    content['score'] = 3
    content['time'] = datetime.datetime.today()
    content['type'] = 'story'
    content['deleted'] = False
    content['poll'] = 222
    content['parts'] = []
    content['parent'] = -1
    return content

def format_comment(content):
    items = db_con.items
    content['id'] = items.count()
    content['descendants'] = 7 #just a number, not sure about This
    content['kids'] = []
    content['score'] = 1
    content['time'] = datetime.datetime.today()
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
    story['by'] = get_user(story['by'])
    story['kids'] = get_comments(story['id'])
    return story

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
                    comment['kids'].append(item)
            arr.append(comment)
    return arr
