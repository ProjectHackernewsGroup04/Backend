import database
import datetime
from bson.json_util import dumps
import pymongo

# Global variables
db_con = database.get_db_conn()


def prepare():
    database.prepare_db()
    print("ASDASD")


def get_latest_id():
    print('Trying getting latest hannestid')
    items = db_con.post
    item_list = items.find_one(sort=[( '_id', pymongo.DESCENDING )] )
    return item_list
