from flask import Flask,request, send_file
from flask_cors import CORS, cross_origin
import os

from Proxies import ImageTagging_class, SendEmail_class, S3
from RabbitMQ import RabbitMQ_Send
from Database import Database_class
db = Database_class()


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
  
  
 
@app.route('/post_submit/', methods=['POST'])
def post_submit():
  # Step 1
  email = request.form['email']
  description= request.form['description']
  image = request.files['image']
  
  # print(image)
  
  # Step 2
  image_type = '.'+image.filename.split('.')[-1]
  # image_type='.'+image_type
  id = db.insert(email=email, description=description, image_type=image_type)
  
  # print(id)
  # save image
  '''create the object name for S3 based on 
  the id and image type for retriving later'''
  obj_name = f'{id}{image_type}' 
  
  image.save(obj_name)
  
  # Step 3
  # send event on queue
  S3().upload_file(obj_name)
  # os.remove(obj_name)
  
  # Step 4
  # RabbitMQ_Send().send(message=f'{id}')
  RabbitMQ_Send().send(message=obj_name)
  
  # Step 5
  return f'Your post was submitted successfully with id <{id}>'


@app.route('/post_view/', methods=['POST'])
def post_view():
  # Step 1
  id = request.form['id'] # get the id from the request
  row_state = db.select_row_by_id(id=id)[0] # get the row from the database
  # Step 2
  '''check if the row is in the database and if the image is ready'''
  
  '''
    0 - is pending 
    1 -  is rejected by the image tagging service
    2 - is accepted and ready
  '''
  
  '''
    row(0) - id
    row(1) - description
    row(2) - email
    row(3) - image_type 
    row(4) - email
    row(5) - category
    row(6) - created_at
    row(7) - image_type
    '''

  if row_state[3]  == 0:
    return 'Your post is still pending'
  # Step 3
  elif row_state[3] == 1: 
    return f'Your post is with id <{id}> is rejected'
  # Step 4
  else:
  # Step 5
    res = f'description: {row_state[1]}\n'
    res+= f'category: {row_state[4]}\n'
    res+= f'state: {row_state[3]}\n'
    # res+= 
     
    image_type = row_state[6]
    # print(image_type)
    obj_format = f'{id}{image_type}'
    FILE_NAME = S3().download_file(object_name=id, image_type=image_type)
    # print(FILE_NAME)
    imge =open(FILE_NAME, 'rb')
    
    return send_file(imge, mimetype='image/jpeg')

  
  
