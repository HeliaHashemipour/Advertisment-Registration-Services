import pika
import sys
import os

from Proxies import ImageTagging_class, SendEmail_class, S3


from Database import Database_class

db = Database_class()
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
            state =0
             # Step 1
            print(" [x] Received %r" % body)
            body = body.decode('utf-8')
            # Step 2
            id = int(body.split('.')[0])
            # print(id)
            image_type = (body.split('.')[1])
            
            file_name = S3().download_file(object_name=id, image_type=image_type)
            
            # Step 3
            tag_name, is_vehicle = S3().download_file(object_name=id, image_type=image_type)
            
            if is_vehicle == True:
                state = 2
                db.update(id=id,state=state,category=tag_name)
                email = db.recieve_email(id=id)
                SendEmail_class().send_simple_message(email=email,
                                                      subject='Your post was approved',
                                                      message=f'Your post with id <{id}> was approved')
            else:
                state = 1
                db.update(id=id,state=state,category=tag_name)
                email = db.recieve_email(id=id)
                SendEmail_class().send_simple_message(email=email,
                                                      subject='Your post was rejected',
                                                      message=f'Your post with id <{id}> was rejected')
            os.remove(file_name)
            print(" [x] Done")
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


# print(RabbitMQ_Receive().receive())


# message = "Hello World!"
# print(RabbitMQ_Send().send(message))
