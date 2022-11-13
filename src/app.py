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
  
  # Step 2
  image_type = image.filename.split('.')[-1]
  id = db.insert(email=email, description=description,extension=image_type)
  # save image
  obj_name = f'{id}.{image_type}'
  image.save(obj_name)
  
  # Step 3
  # send event on queue
  S3().upload_file(obj_name)
  os.remove(obj_name)
  
  # Step 4
  RabbitMQ_Send().send(message=obj_name)
  
  # Step 5
  return f'Your post was submitted successfully with id <{id}>'


@app.route('/post_view/', methods=['POST'])
def post_view():
  id = request.form['id']
  


  
  
