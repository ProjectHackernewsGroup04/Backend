# consume.py
import pika, os
import controller
import os
import time

url = os.environ.get('amqp://dkwttbup:6l_JoEG8FQQNFR-Imf-FWzs8H2avSPhe@lion.rmq.cloudamqp.com/dkwttbup', 'rabbitmq')
time.sleep(10)
#params = pika.URLParameters(url)
local = pika.ConnectionParameters('rabbitmq')
connection = pika.BlockingConnection(local)
channel = connection.channel()


# Callback function - Executes for each message we consumes
def callback(ch, method, properties, body):
  print(" [x] Received %r" % body)
  controller.add_post(body)

channel.basic_consume(callback,
                      queue='Helge-api-posts',
                      no_ack=True)

# Run rabbitmq consumer
if __name__ == '__main__':
    print(' [*] RabbitMQ consumer: Waiting for messages:')
    channel.start_consuming()
