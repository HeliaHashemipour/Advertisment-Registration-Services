import pika
import sys
import os


class RabbitMQ_Send():
    def __init__(self, AMQP_URL, ROUTING_KEY):
        self.AMQP_URL = AMQP_URL
        self.ROUTING_KEY = ROUTING_KEY
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.AMQP_URL))
        self.channel = self.connection.channel()

    def send(self, message):
        self.channel.queue_declare(queue=message)
        self.channel.basic_publish(
            exchange='', routing_key=self.ROUTING_KEY, body=message)
        print(" [x] Sent %r" % message)
        # self.connection.close()


AMQP_URL = "amqps://vyxkmseh:xuftvWWjW2mJkjicdYCyoYp6iZMDvlJb@albatross.rmq.cloudamqp.com/vyxkmseh"
ROUTING_KEY = "hello"
message = "Hello World!"
print(RabbitMQ_Send(AMQP_URL, ROUTING_KEY).send(message))
