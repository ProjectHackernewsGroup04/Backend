from pymongo import MongoClient

clientLocalhost = MongoClient('localhost', 27017)

# Docker database setup
client = MongoClient('db', 27017)
db = client.hackernews
user_coll = db.users
item_coll = db.items

# ---------------------------------------------------------------
# Database names
db_name = "hackernews"
collection_name_items = "items"
collection_name_users = "users"
sample_data = {"id": 1, "by": "TestUser", "type": "story"}


def get_db_conn():
    connection = client[db_name]
    return connection


def prepare_db():
    db_con = get_db_conn()
    item_coll = db_con[collection_name_items]
    user_coll = db_con[collection_name_users]

    # Checking if the collection is empty
    if item_coll.count() == 0:
        print("Database is empty, adding sample data")
        item_coll.insert_one(sample_data)
        print("Sample data added in database")
    print("Connection to DB succeeded")
