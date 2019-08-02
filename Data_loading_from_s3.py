import boto3
import re
import requests
import json
from requests_aws4auth import AWS4Auth
region='<region>'
service = '<service>'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
host = '' # the Amazon ES domain, including https://
index = 'lambda-s3-index'
type = 'lambda-type'
url = host + '/' + index + '/' + type
headers = { "Content-Type": "application/json" }
s3 = boto3.resource('s3')
def handler(event,context):
    bucket_name=event["bucket_name"]
    folder_name=event["folder_name"]
    bucket=s3.Bucket(bucket_name)
    for files in bucket.objects.filter(Prefix=folder_name):
        file_content = files.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        lines = file_content.splitlines()
        r = requests.post(url, auth=awsauth, json=json_content, headers=headers)

