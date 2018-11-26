import logging
import sys
from logstash_async.handler import AsynchronousLogstashHandler

try:
    host = 'logstash'
    port = 5005
    test_logger = logging.getLogger('logstash')
    test_logger.setLevel(logging.INFO)
    test_logger.addHandler(AsynchronousLogstashHandler(
    host, port, database_path='logstash.db'))
except:
	print("except")

# If you don't want to write to a SQLite database, then you do
# not have to specify a database_path.
# NOTE: Without a database, messages are lost between process restarts.
# test_logger.addHandler(AsynchronousLogstashHandler(host, port))

def log_info_extra(msg,extra):
    try:
        test_logger.info(msg,extra=extra)
    except:
        print("wtf")

def log_info(msg):
    try:
        test_logger.info(msg)
    except:
        print("wtf")

def log_error(msg):
    try:
        test_logger.error(msg)
    except:
        print("wtf")


