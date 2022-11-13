import requests
import pika
import json
import logging
import boto3
from botocore.exceptions import ClientError
import os

API_KEY_IMAGE = 'acc_de10f3569b04ef6'
API_SECRET_IMAGE = 'b1728fcb6d7f5a9ad0824c8e354e0817'
IMAGE_URL = 'https://wallpapercave.com/wp/wp3503654.jpg'

DOMAIN = "sandbox946608aa307241419f0a093a1fdd500c.mailgun.org"
API_KEY_EMAIL = "818378731d5374cd733ec4f5c5abf6c4-48c092ba-a51fd35d"
EMAIL_ADDRESS = "heliahashemipour2@gmail.com"
TEXT = "Your ad has been accepted!"
SUBJECT = "Cloud Computing HW1"

AMQP_URL = "amqps://vyxkmseh:xuftvWWjW2mJkjicdYCyoYp6iZMDvlJb@albatross.rmq.cloudamqp.com/vyxkmseh"
ROUTING_KEY = "hello"
message = 1


class ImageTagging_class:
    def __init__(self, API_KEY_IMAGE, API_SECRET_IMAGE):
        self.API_KEY_IMAGE = API_KEY_IMAGE
        self.API_SECRET_IMAGE = API_SECRET_IMAGE
        self.IMAGE_URL = IMAGE_URL

    @staticmethod
    def tagging_obj(IMAGE_URL):
        response = requests.get(
            'https://api.imagga.com/v2/tags?image_url=%s' % IMAGE_URL,
            auth=(API_KEY_IMAGE, API_SECRET_IMAGE))

        tags = response.json()['result']['tags']
        for tag in tags:
            confidence = tag['confidence']
            tag_name = tag['tag']['en']
            print(f'Confidence: {confidence}, tag: {tag_name}')

        return tag_name, confidence


tag_name, confidence = ImageTagging_class(
    API_KEY_IMAGE, API_SECRET_IMAGE).tagging_obj(IMAGE_URL)
print(tag_name, confidence)

# print(image.taggin g_obj())


class SendEmail_class:
    def __init__(self, DOMAIN, API_KEY_EMAIL, EMAIL_ADDRESS, TEXT, SUBJECT):
        self.DOMAIN = DOMAIN
        self.API_KEY_EMAIL = API_KEY_EMAIL
        self.EMAIL_ADDRESS = EMAIL_ADDRESS
        self.TEXT = TEXT
        self.SUBJECT = SUBJECT

    @staticmethod
    def send_simple_message(email, subject, text):
        return requests.post(
            f"https://api.mailgun.net/v3/{DOMAIN}/messages",
            auth=("api", API_KEY_EMAIL),
            data={"from": f"<mailgun@{DOMAIN}>",
                  "to": [email],
                  "subject": subject,
                  "text": text})

    def send_response(self):
        response = self.send_simple_message(
            self.EMAIL_ADDRESS, self.SUBJECT, self.TEXT)
        # print(response.json())
        return response.json()


class RABBIT:
    _channel = None

    @classmethod
    def channel(cls):
        if cls._channel is None:
            params = pika.URLParameters(AMQP_URL)
            Connection = pika.BlockingConnection(params)
            cls._channel = Connection.channel()
            cls._channel.queue_declare(queue='posts')
        return cls._channel

    @classmethod
    def publish(cls, post_id: int):
        channel = cls.channel()  # type: pika.adapters.blocking_connection.BlockingChannel
        cls.channel().basic_publish(
            exchange='', routing_key='posts', body=json.dumps({'post_id': post_id}))
        print(f'Post <{post_id}> has been sent to the queue')


 
class Post:
    def __init__(self, post_id: int):
        self.post_id = post_id

    def publish(self):
        RABBIT.publish(self.post_id)


email_response = SendEmail_class(
    DOMAIN, API_KEY_EMAIL, EMAIL_ADDRESS, TEXT, SUBJECT).send_response()

print(email_response)
# post = Post(1)
# print(post.publish())

# print(image.tagging_obj())


class S3:
    def __init__(self, bucket_name, file_name, object_name=None):
        self.bucket_name = bucket_name
        self.file_name = file_name
        self.object_name = object_name
        
    def upload_file(file_name, bucket, object_name=None):

    # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

    # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

url = 'https://firstassignment.s3.ir-thr-at1.arvanstorage.com'
s3 = S3(url, 'test.txt')

print(s3.upload_file('test.txt', url))