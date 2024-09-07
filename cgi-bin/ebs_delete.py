#!/usr/bin/env python3

import cgi
import cgitb
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

cgitb.enable()

def delete_ebs_volume(volume_id, region, aws_access_key, aws_secret_key):
    try:
        ec2 = boto3.client('ec2',
                           region_name=region,
                           aws_access_key_id=aws_access_key,
                           aws_secret_access_key=aws_secret_key)
        response = ec2.delete_volume(
            VolumeId=volume_id
        )
        return f"Successfully deleted volume {volume_id}"
    except NoCredentialsError:
        return "Error: AWS credentials not found."
    except PartialCredentialsError:
        return "Error: Incomplete AWS credentials."
    except Exception as e:
        return f"Error: {str(e)}"

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
volume_id = form.getvalue("volumeId")
region = form.getvalue("region")
aws_access_key = form.getvalue("awsAccessKey")
aws_secret_key = form.getvalue("awsSecretKey")

if volume_id and region and aws_access_key and aws_secret_key:
    result = delete_ebs_volume(volume_id, region, aws_access_key, aws_secret_key)
else:
    result = "Error: Missing required form data."

print(result)

