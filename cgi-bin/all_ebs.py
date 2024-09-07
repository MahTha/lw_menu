#!/usr/bin/env python3

import cgi
import cgitb
import boto3
import time

cgitb.enable()

print("Content-type: text/html\n")

# Retrieve form data
form = cgi.FieldStorage()
access_key = form.getvalue("access_key")
secret_key = form.getvalue("secret_key")
region = form.getvalue("region")
availability_zone = form.getvalue("availability_zone")
size = int(form.getvalue("size"))
volume_type = form.getvalue("volume_type")
instance_id = form.getvalue("instance_id")
device_name = form.getvalue("device_name")

try:
    # Create a session using provided AWS credentials
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    # Create EC2 client
    ec2_client = session.client('ec2')

    # Step 1: Create a new EBS volume
    response = ec2_client.create_volume(
        AvailabilityZone=availability_zone,
        Size=size,
        VolumeType=volume_type
    )

    volume_id = response['VolumeId']
    print(f"<p>Created volume {volume_id}.</p>")

    # Step 2: Wait for the volume to become available
    while True:
        volume = ec2_client.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
        state = volume['State']
        if state == 'available':
            break
        print(f"<p>Volume {volume_id} is {state}. Waiting...</p>")
        time.sleep(5)

    # Step 3: Attach the volume to the instance
    ec2_client.attach_volume(
        VolumeId=volume_id,
        InstanceId=instance_id,
        Device=device_name
    )

    print(f"<p>Attached volume {volume_id} to instance {instance_id} as {device_name}.</p>")

except Exception as e:
    print(f"<p>Error: {str(e)}</p>")

