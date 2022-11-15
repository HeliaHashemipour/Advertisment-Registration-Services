import pika
import sys
import os

from Proxies import ImageTagging_class, SendEmail_class, S3


from Database import Database_class

db = Database_class()
class RabbitMQ_Send:
    def __init__(self):
        self.AMQP_URL = "amqps://vyxkmseh:xuftvWWjW2mJkjicdYCyoYp6iZMDvlJb@albatross.rmq.cloudamqp.com/vyxkmseh"
        self.ROUTING_KEY = "hello"
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.AMQP_URL))
        self.channel = self.connection.channel()

    def send(self, message):
        self.channel.queue_declare(queue='hello') # make sure the queue exists
        self.channel.basic_publish(
            exchange='', routing_key=self.ROUTING_KEY, body=message) # send the message
        print(" [x] Sent %r" % message)
        # self.connection.close()


class RabbitMQ_Receive:
    def __init__(self):
        self.AMQP_URL = "amqps://vyxkmseh:xuftvWWjW2mJkjicdYCyoYp6iZMDvlJb@albatross.rmq.cloudamqp.com/vyxkmseh"
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.AMQP_URL))
        self.channel = self.connection.channel()
        self.queue = "hello"

    def receive(self):
        self.channel.queue_declare(queue=self.queue) # declare the queue
  
        def callback(ch, method, properties, body): 
            state = 0 # by default, the state is 0
            
             # Step 1
            print(" [x] Received %r" % body) # print the message
            body = body.decode('utf-8') # convert the message to string
            # len(body.encode('utf-8')) 
            
            # Step 2
            # print(body)
            id = int(body.split('.')[0])  # get the id from the message
            # print(id)
            image_type ='.'+ (body.split('.')[1])  # get the image type from the message
            file_name =  S3().download_file(object_name=id, image_type=image_type) # download the image from S3
            # print(file_name)
            
            # Step 3
            tag_name, is_vehicle = ImageTagging_class().tagging_obj(file_name) # tag the image
            # print(is_vehicle)
            
            if is_vehicle == True:
                state = 2
                db.update(id=id,state=state,category=tag_name) # update the database
                email = db.recieve_email(id=id)
                SendEmail_class().send_simple_message(email=email,
                                                      subject='Your post was approved',
                                                      text=f'Your post with id <{id}> was approved') # send email
                print('approved')
            else:
                state = 1
                db.update(id=id,state=state,category=tag_name) # update the database
                email = db.recieve_email(id=id) # update the database
                SendEmail_class().send_simple_message(email=email,
                                                      subject='Your post was rejected',
                                                      text=f'Your post with id <{id}> was rejected') # send email
                print('rejected')
            # os.remove(file_name) # remove the image from the server
            print(" [x] Done")
            # ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback, auto_ack=True) # consume the message
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming() # start consuming


# print(RabbitMQ_Receive().receive())


# message = "41.jpg"
# (RabbitMQ_Send().send(message))


# RabbitMQ_Receive().receive()

# # RabbitMQ_Receive()
# message = "12.jpg"
# RabbitMQ_Send().send(message)