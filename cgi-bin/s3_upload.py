#!/usr/bin/env python3

import cgi
import cgitb
import boto3
import os

cgitb.enable()

print("Content-type: text/html\n")

# Retrieve form data
form = cgi.FieldStorage()
access_key = form.getvalue("access_key")
secret_key = form.getvalue("secret_key")
region = form.getvalue("region")
bucket_name = form.getvalue("bucket_name")
fileitem = form['file']

if fileitem.filename:
    try:
        # Get the file data and file name
        filename = os.path.basename(fileitem.filename)
        file_data = fileitem.file.read()

        # Create a session using provided AWS credentials
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        # Create S3 client
        s3_client = session.client('s3')

        # Upload the file to S3
        s3_client.put_object(Bucket=bucket_name, Key=filename, Body=file_data)

        print(f"<p>Successfully uploaded {filename} to {bucket_name}.</p>")

    except Exception as e:
        print(f"<p>Error: {str(e)}</p>")

else:
    print("<p>No file was uploaded.</p>")

