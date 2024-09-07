#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3
from botocore.exceptions import ClientError

cgitb.enable()

# AWS Credentials
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

print("Content-Type: application/json\n")

form = cgi.FieldStorage()
bucket_name = form.getvalue('bucketName')
aws_region = form.getvalue('awsRegion')

if not bucket_name:
    print(json.dumps({'error': 'Bucket name is required'}))
    exit()

if not aws_region:
    print(json.dumps({'error': 'AWS region is required'}))
    exit()

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=aws_region)

try:
    s3.delete_bucket(Bucket=bucket_name)
    print(json.dumps({'message': 'Bucket deleted successfully!'}))
except ClientError as e:
    print(json.dumps({'error': str(e)}))

