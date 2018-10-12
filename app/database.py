from pymongo import MongoClient

# Database names
client = MongoClient('database', 27017)
db_name = "hackernews"
collection_name_items = "items"
collection_name_users = "users"
collection_name_posts = "posts"
sample_user = {"userID": 1, "username": "TestUser", "password": "1234"}


# Get the connection instance
def get_db_conn():
    connection = client[db_name]
    return connection

