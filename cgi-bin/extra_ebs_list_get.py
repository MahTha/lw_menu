#!/usr/bin/env python3

import cgi
import cgitb
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from datetime import datetime

cgitb.enable()

def get_volume_details(volume_id, region, aws_access_key, aws_secret_key):
    try:
        ec2 = boto3.client('ec2',
                           region_name=region,
                           aws_access_key_id=aws_access_key,
                           aws_secret_access_key=aws_secret_key)
        response = ec2.describe_volumes(VolumeIds=[volume_id])
        volume = response.get('Volumes', [])[0]
        
        volume_details = {
            'VolumeId': volume['VolumeId'],
            'Size': volume['Size'],
            'State': volume['State'],
            'VolumeType': volume['VolumeType'],
            'IOPS': volume['Iops'],
            'AvailabilityZone': volume['AvailabilityZone'],
            'SnapshotId': volume.get('SnapshotId', 'N/A'),
            'CreateTime': volume['CreateTime'],
            'Attachments': volume['Attachments']
        }

        details_html = f"""
        <h2>Volume Details for {volume_id}</h2>
        <ul>
            <li>Size: {volume_details['Size']} GiB</li>
            <li>State: {volume_details['State']}</li>
            <li>Volume Type: {volume_details['VolumeType']}</li>
            <li>IOPS: {volume_details['IOPS']}</li>
            <li>Availability Zone: {volume_details['AvailabilityZone']}</li>
            <li>Snapshot ID: {volume_details['SnapshotId']}</li>
            <li>Create Time: {volume_details['CreateTime'].strftime('%Y-%m-%d %H:%M:%S')}</li>
        </ul>
        """

        if volume_details['Attachments']:
            attachment = volume_details['Attachments'][0]
            details_html += f"""
            <h3>Attachment Details</h3>
            <ul>
                <li>Instance ID: {attachment['InstanceId']}</li>
                <li>Device: {attachment['Device']}</li>
                <li>Attach Time: {attachment['AttachTime'].strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li>State: {attachment['State']}</li>
            </ul>
            """
        else:
            details_html += "<p>No attachments found for this volume.</p>"

        return details_html
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
    result = get_volume_details(volume_id, region, aws_access_key, aws_secret_key)
else:
    result = "Error: Missing required form data."

print(result)

