import bcrypt
import database
import datetime
import pymongo
from bson.json_util import dumps

# Global variables
db_con = database.get_db_conn()

# TODO