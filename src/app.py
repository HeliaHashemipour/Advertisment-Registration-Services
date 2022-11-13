from flask import Flask,request, send_file
from flask_cors import CORS, cross_origin
import os

from proxies import ImageTagging_class, SendEmail_class, S3
from RabbitMQ import RabbitMQ_Send
from Database import Database_class

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
  
