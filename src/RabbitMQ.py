import pika
import sys
import os


class RabbitMQ_Send():
    def __init__(self):
        self.AMQP_URL = "amqps://vyxkmseh:xuftvWWjW2mJkjicdYCyoYp6iZMDvlJb@albatross.rmq.cloudamqp.com/vyxkmseh"
        self.ROUTING_KEY = "hello"
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.AMQP_URL))
        self.channel = self.connection.channel()

    def send(self, message):
        self.channel.queue_declare(queue='hello')
        self.channel.basic_publish(
            exchange='', routing_key=self.ROUTING_KEY, body=message)
        print(" [x] Sent %r" % message)
        # self.connection.close()


class RabbitMQ_Receive():
    def __init__(self):
        self.AMQP_URL = "amqps://vyxkmseh:xuftvWWjW2mJkjicdYCyoYp6iZMDvlJb@albatross.rmq.cloudamqp.com/vyxkmseh"
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.AMQP_URL))
        self.channel = self.connection.channel()
        self.queue = "hello"

    def receive(self):
        self.channel.queue_declare(queue=self.queue)

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


# print(RabbitMQ_Receive().receive())


# message = "Hello World!"
# print(RabbitMQ_Send().send(message))
