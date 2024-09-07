#!/usr/bin/env python3

import cgi
import cgitb
import json
import boto3
from botocore.exceptions import ClientError

cgitb.enable()  # Enable debugging

def main():
    print("Content-Type: application/json")
    print()  # End of headers

    form = cgi.FieldStorage()
    region = form.getvalue('region')
    aws_access_key_id = form.getvalue('aws_access_key_id')
    aws_secret_access_key = form.getvalue('aws_secret_access_key')
    instance_id = form.getvalue('instance_id')

    if not (region and aws_access_key_id and aws_secret_access_key and instance_id):
        response = {"error": "All fields are required"}
        print(json.dumps(response))
        return

    try:
        ec2 = boto3.client(
            "ec2",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        ec2.terminate_instances(InstanceIds=[instance_id])
        response = {"success": f"Instance {instance_id} terminated successfully!"}
    except ClientError as e:
        response = {"error": str(e)}

    print(json.dumps(response))

if __name__ == "__main__":
    main()

