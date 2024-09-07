#!/usr/bin/env python3

import boto3
import json
import cgi
import cgitb

cgitb.enable(display=0, logdir="/path/to/logdir")  # Enable debugging to a log file

# Hard-coded AWS credentials (not recommended for production)
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

print("Content-Type: application/json")
print()

try:
    # Get the form data
    form = cgi.FieldStorage()

    size = form.getvalue('size')
    availability_zone = form.getvalue('availability_zone')
    volume_type = form.getvalue('volume_type', 'gp2')  # Default to 'gp2' if not provided

    # Create an EC2 client
    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=availability_zone[:-1]  # Extract region from availability zone
    )

    # Create the EBS volume
    response = ec2.create_volume(
        Size=int(size),
        AvailabilityZone=availability_zone,
        VolumeType=volume_type
    )

    # Return the response as JSON
    print(json.dumps(response, default=str))

except Exception as e:
    print(json.dumps({'error': str(e)}))
