#!/usr/bin/env python3

import boto3
import json
import cgi
import cgitb
cgitb.enable()

print("Content-Type: text/html\n")

# Parse form data
form = cgi.FieldStorage()
bucket_name = form.getvalue('bucket')
access_key = form.getvalue('accessKey')
secret_key = form.getvalue('secretKey')

# Initialize a session using Amazon S3 with provided credentials
s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Call S3 to list objects in the selected bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Get a list of object keys from the response
objects = []
if 'Contents' in response:
    objects = [obj['Key'] for obj in response['Contents']]

# Print out the object list as a JSON object
print(json.dumps(objects))

