from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# Database names
db_name = "hackernews"
collection_name_items = "items"
collection_name_users = "users"
sample_data = {"id": 1, "by": "TestUser", "type": "story"}


def get_db_conn():
    print(client.list_database_names())
    connection = client[db_name]
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
