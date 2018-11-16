import logging
import sys
from logstash_async.handler import AsynchronousLogstashHandler

host = 'logstash'
port = 5005

test_logger = logging.getLogger('logstash')
test_logger.setLevel(logging.INFO)
test_logger.addHandler(AsynchronousLogstashHandler(
    host, port, database_path='logstash.db'))

# If you don't want to write to a SQLite database, then you do
# not have to specify a database_path.
# NOTE: Without a database, messages are lost between process restarts.
# test_logger.addHandler(AsynchronousLogstashHandler(host, port))

def log_info_extra(msg,extra):
    test_logger.info(msg,extra=extra)

def log_info(msg):
    test_logger.info(msg)
    print("ASD",flush=True)

