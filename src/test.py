
import boto3
import logging 

logging.basicConfig(level=logging.INFO)

try:
    s3_resource = boto3.resource(
        's3',
        endpoint_url='endpoint_url',
        aws_access_key_id='access_key',
        aws_secret_access_key='secret_key'
    )
except Exception as exc:
    logging.info(exc)