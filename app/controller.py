import bcrypt
import database
import pymongo
import datetime
from bson.json_util import dumps

# Global variables
db_con = database.get_db_conn()
items = db_con.items
users = db_con.users


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
    if items.insert(story):
        print('Added', story['id'])
        return story
    else:
        print('Can\'t add story')
        return False


def get_all_items():
    print('Trying getting all items')
    itemList = items.find({'type': 'story'})
    return itemList


def get_item_by_id(id):
    print('Trying getting one item by ID')
    itemList = items.find_one({"id": id})
    return itemList


def delete_item_by_id(id):
    print('Trying delete item by ID')
    item = items.find_one({"id":id})
    if item:
        items.update_one({"id": id},
            {'$set': {'deleted': True}}, upsert=False)
        return True
    else:
        return False

def add_comment(content):
    print('Trying to add comment to DB on ', content['by'])
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
    if items.update({"id": parent},
        {'$push': { "kids": child }}):
        return construct_story(parent)
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
    content['id'] = items.count()
    content['descendants'] = 7 #just a number, not sure about This
    content['kids'] = []
    content['score'] = 1
    content['time'] = datetime.datetime.today()
    content['type'] = 'comment'
    content['deleted'] = False
    content['poll'] = 222
    content['parts'] = []
    return content

def construct_story(id):
    story = items.find_one({"id":id})
    story['by'] = get_user(story['by'])
    story['kids'] = get_comments(story['id'])
    return story

def get_user(username):
    return users.find_one({"username": username})

def get_comments(parent):
    comments = items.find({"parent": parent})
    nested = []
    for i in range(0,comments.count()-1):
        if len(comments[i]['kids']) > 0:
            nested = nested.append(get_comments(comments[i]['id']))
            comments[i]['kids'] = nested
    return comments

# def build_nested_comments(kids):
#     for i in range(0, kids.count()):
#         if len(kids[i]['kids']) > 0:
#             children = items.find({"parent": kids[i]['id']}) #Find all who's parent is this comment
#             kids[i]['kids'] = build_nested_comments(children)
#     print('COMMENTS----->', dumps(kids))
#     return kids

# def get_user_for_comments(kids):
#     for i in range(0,kids.count()-1):
#         kids[i]['by'] = get_user(kids[i]['by'])
#     print('SHITY', dumps(kids))
#     return kids
