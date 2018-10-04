from pymongo import MongoClient

# Database names
db_name = "hackernews"
collection_name_items = "items"
collection_name_users = "users"
sample_user = {"userID": 1, "username": "TestUser", "password": "1234"}


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
        # user_coll.insert_one(sample_user)
        # item_coll.insert_many(data)
        print("Sample data added in database")


print("Connection to DB succeeded")
