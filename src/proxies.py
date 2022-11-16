import requests
import logging
import boto3
from botocore.exceptions import ClientError
import os


'''
This class is responsible for uploading the image to S3 and
downloading the image from S3 to the local machine
and tag the image using Imagga API
and send the email using Mailgun API
'''
logging.basicConfig(level=logging.INFO)


API_KEY_IMAGE = 'acc_de10f3569b04ef6'
API_SECRET_IMAGE = 'b1728fcb6d7f5a9ad0824c8e354e0817'
IMAGE_URL = 'https://wallpapercave.com/wp/wp3503654.jpg'

# DOMAIN = "sandbox946608aa307241419f0a093a1fdd500c.mailgun.org"
# API_KEY_EMAIL = "818378731d5374cd733ec4f5c5abf6c4-48c092ba-a51fd35d"
EMAIL_ADDRESS = "heliahashemipour@aut.ac.ir"
# TEXT = "Your ad has been accepted!"
# SUBJECT = "Cloud Computing HW1"

AMQP_URL = "amqps://vyxkmseh:xuftvWWjW2mJkjicdYCyoYp6iZMDvlJb@albatross.rmq.cloudamqp.com/vyxkmseh"
ROUTING_KEY = "hello"
# message = 1


class ImageTagging_class:
    def __init__(self):
        self.API_KEY_IMAGE = 'acc_f101cd22c43c79c'
        self.API_SECRET_IMAGE = 'cc6149264bd911e364a0a58c6b2127aa'
        # self.IMAGE_URL = IMAGE_URL

    def tagging_obj(self, image_path):
        IMAGE_URL = 'https://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'
        # print(image_path)
        # image_pathh = '/Users/heliaa/University/Semester7/Cloud/PRJ1/src/'+image_path 
        # response = requests.post(
        #     'https://api.imagga.com/v2/tags',
        #     auth=(self.API_KEY_IMAGE, self.API_SECRET_IMAGE),
        #     files={'image': open(image_path, 'rb')}
        #     )
        response = requests.get(
            'https://api.imagga.com/v2/tags?image_url=%s' % IMAGE_URL,
            auth=(self.API_KEY_IMAGE, self.API_SECRET_IMAGE))


        # print(response.json())
        is_vehicle = False
        
        tags = response.json()['result']['tags']  # list of tags
        
        for tag in tags:
            if  tag['tag']['en'] == 'vehicle':
                is_vehicle = True  # if vehicle is in the tags, then it is a vehicle
                break
            
        tags = response.json()['result']['tags'][0]
        confidence = tags['confidence'] # confidence of the tag
        tag_name = tags['tag']['en'] # tag name 
        print(f'tag: {tag_name}') # print the tag and its confidence
            
        print(f'is vehicle: {is_vehicle}') # print if it is a vehicle or not

        return tag_name, is_vehicle



# checked
# tag_name, confidence = ImageTagging_class(
#     API_KEY_IMAGE, API_SECRET_IMAGE).tagging_obj(IMAGE_URL)
# print(tag_name, confidence)

# print(image.taggin g_obj())
# image_path = '/Users/heliaa/University/Semester7/Cloud/PRJ1/src/49.jpg'
# tag_name, is_vehicle=ImageTagging_class().tagging_obj(image_path)
# print(ImageTagging_class().tagging_obj(image_path))



class SendEmail_class:
    def __init__(self):
        self.DOMAIN = "sandbox2c66c8ba08704e23ba2ee5a08e0eb08a.mailgun.org"
        self.API_KEY_EMAIL = "91d1efd9903f3dd0c627b3bc30c341e8-2de3d545-1257bc0e"
        # self.EMAIL_ADDRESS = EMAIL_ADDRESS
        # self.TEXT = TEXT
        # self.SUBJECT = SUBJECT

    def send_simple_message(self, email, subject, text):
        return requests.post(
            f"https://api.mailgun.net/v3/{self.DOMAIN}/messages",
            auth=("api", self.API_KEY_EMAIL),
            data={"from": f"<mailgun@{self.DOMAIN}>",
                  "to": [email],
                  "subject": subject,
                  "text": text})

    def send_response(self, email, subject, text):
        response = self.send_simple_message(email, 
                                            subject, 
                                            text) # send email
        # print(response.json())
        return response.json()
    
    
# checked

# response = SendEmail_class().send_simple_message(EMAIL_ADDRESS, SUBJECT, TEXT)
# print(response.json())


class S3:
    def __init__(self):
        self.bucket_name = 'hw1cloudcomputing'
        self.s3_client = boto3.client(
            's3',
            endpoint_url='https://hw1cloudcomputing.s3.ir-thr-at1.arvanstorage.com',
            aws_access_key_id='6d04e8b0-645e-4a26-b9e0-128f830a36ce',
            aws_secret_access_key='e2b5741fc6c88d35c6f6c2dc0cdcedfb84d994fa'
        )

    def upload_file(self, file_name, object_name=None):
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name) # get the file name
        # print(file_name)

    # Upload the file
        # s3_client = boto3.client('s3')
        try:
            response = self.s3_client.upload_file(file_name, 
                                                  self.bucket_name,
                                                  object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    def download_file( self, object_name, image_type):
        # If S3 object_name was not specified, use file_name
        # print(file_name)
        filename = f'/Users/heliaa/University/Semester7/Cloud/PRJ1/src/{object_name}{image_type}' # path to save the image
        obj_path = f'{object_name}{image_type}'  # object name in s3
        object_name = os.path.basename(filename) # get the file name
        self.s3_client.download_file(self.bucket_name,
                                     obj_path,
                                     filename
                                     ) # download the image
        
        # s3 = boto3.client('s3')
        # with open('FILE_NAME', 'wb') as f:
        #     s3.download_fileobj('BUCKET_NAME', 'OBJECT_NAME', f)
        return filename
    
    def create_presigned_url(self, object_name):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.bucket_name,
                                                                'Key': object_name})
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response
    
    def accessing(self):
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)


# checked

# url = 'https://firstassignment.s3.ir-thr-at1.arvanstorage.com'
# s3 = S3(url, 'test.txt')
# print(s3.upload_file('test.txt', url))
# S3().upload_file('/Users/heliaa/University/Semester7/Cloud/PRJ1/src/13.jpg')
# print(S3().create_presigned_url('53.jpg'))


# S3().accessing()