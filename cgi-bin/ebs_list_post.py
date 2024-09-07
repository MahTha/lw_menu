#!/usr/bin/env python3

import cgi
import cgitb
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

cgitb.enable()

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
region = form.getvalue("region")
aws_access_key = form.getvalue("awsAccessKey")
aws_secret_key = form.getvalue("awsSecretKey")

if region and aws_access_key and aws_secret_key:
    try:
        ec2 = boto3.client('ec2',
                           region_name=region,
                           aws_access_key_id=aws_access_key,
                           aws_secret_access_key=aws_secret_key)
        response = ec2.describe_volumes()
        volumes = response.get('Volumes', [])

        if volumes:
            print("<h2>Available EBS Volumes</h2>")
            print("<ul>")
            for volume in volumes:
                volume_id = volume['VolumeId']
                print(f'<li><a href="javascript:getVolumeDetails(\'{volume_id}\')">{volume_id}</a></li>')
            print("</ul>")
        else:
            print("No volumes found.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
    except Exception as e:
        print(f"Error: {str(e)}")
else:
    print("Error: Missing required form data.")

