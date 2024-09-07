#!/usr/bin/env python3

import cgi
import cgitb
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

cgitb.enable()

def attach_ebs_volume(volume_id, instance_id, device_name, region, aws_access_key, aws_secret_key):
    try:
        ec2 = boto3.client('ec2',
                           region_name=region,
                           aws_access_key_id=aws_access_key,
                           aws_secret_access_key=aws_secret_key)
        response = ec2.attach_volume(
            VolumeId=volume_id,
            InstanceId=instance_id,
            Device=device_name
        )
        return f"Successfully attached volume {volume_id} to instance {instance_id} on device {device_name}"
    except NoCredentialsError:
        return "Error: AWS credentials not found."
    except PartialCredentialsError:
        return "Error: Incomplete AWS credentials."
    except Exception as e:
        return f"Error: {str(e)}"

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
volume_id = form.getvalue("volumeId")
instance_id = form.getvalue("instanceId")
device_name = form.getvalue("deviceName")
region = form.getvalue("region")
aws_access_key = form.getvalue("awsAccessKey")
aws_secret_key = form.getvalue("awsSecretKey")

if volume_id and instance_id and device_name and region and aws_access_key and aws_secret_key:
    result = attach_ebs_volume(volume_id, instance_id, device_name, region, aws_access_key, aws_secret_key)
else:
    result = "Error: Missing required form data."

print(result)

