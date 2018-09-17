from pymongo import MongoClient

# Database names
db_name = "hackernews"
collection_name_items = "items"
collection_name_users = "users"
sample_data = {"id": 1, "by": "TestUser", "type": "story"}


def get_db_conn():
    my_client = MongoClient('db', 27017)
    print(my_client.list_database_names())
    connection = my_client[db_name]
    return connection


def prepare_db():
    db_con = get_db_conn()
    col = db_con[collection_name_items]
    # Checking if the collection is empty
    if col.count() == 0:
        print("Database is empty, adding sample data")
        col.insert_one(sample_data)
        print("Sample data added in database")
    print("Connection to DB succeeded")
