#!/usr/bin/env python3

import boto3
import json
import cgi
import cgitb
cgitb.enable()

print("Content-Type: text/html\n")

# Parse form data
form = cgi.FieldStorage()
access_key = form.getvalue('accessKey')
secret_key = form.getvalue('secretKey')

# Initialize a session using Amazon S3 with provided credentials
s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

# Print out the bucket list as a JSON object
print(json.dumps(buckets))

