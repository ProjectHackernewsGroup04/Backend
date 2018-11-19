from pymongo import MongoClient
import datetime, time
from log import log_handler as log

# Database names
client = MongoClient('database', 27017)
db_name = "hackernews"
collection_name_items = "items"
collection_name_users = "users"
collection_name_posts = "posts"
sample_user = {"userID": 1, "username": "TestUser", "password": "1234"}


def get_db_conn():
    connection = client[db_name]
    return connection


def prepare_db():
    try:
        db_con = get_db_conn()
    except Exception as e:
        log.log_error("DATABASE ERROR",e)
    
    item_coll = db_con[collection_name_items]
    user_coll = db_con[collection_name_users]
    posts_coll = db_con[collection_name_posts]

    # Checking if the collection is empty
    if item_coll.count() == 0:
        print("Database is empty, adding sample data")
        posts_coll.insert_one({'added': datetime.datetime.fromtimestamp(time.time())})
        # user_coll.insert_one(sample_user)
        # item_coll.insert_many(data)
        print("Sample data added in database")


    print("Connection to DB succeeded")
