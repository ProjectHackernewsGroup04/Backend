# consume.py
import pika, os
import controller

# Establish a connection with RabbitMQ server.
url = 'amqp://dkwttbup:6l_JoEG8FQQNFR-Imf-FWzs8H2avSPhe@lion.rmq.cloudamqp.com/dkwttbup'
params = pika.URLParameters(url)
#local = pika.ConnectionParameters('rabbitmq')
connection = pika.BlockingConnection(params)
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
