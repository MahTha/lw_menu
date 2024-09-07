#!/usr/bin/python3

import boto3
import json
import os
import sys

# Configuration
AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
S3_BUCKET_NAME = 'maheshthapa01'

# Initialize AWS clients
transcribe = boto3.client('transcribe', region_name=AWS_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

# Read JSON input from CGI POST request
try:
    content_length = int(os.environ.get('CONTENT_LENGTH', 0))
    post_data = sys.stdin.read(content_length)
    json_data = json.loads(post_data)
    object_key = json_data.get('objectKey', '')

    if not object_key:
        raise ValueError('No S3 object key provided.')

    # Start transcription job
    job_name = 'transcribe-job-' + os.path.basename(object_key)
    job_uri = f's3://{S3_BUCKET_NAME}/{object_key}'

    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=object_key.split('.')[-1],  # Determine format based on file extension
        LanguageCode='en-US'  # Specify language code if necessary
    )

    print(f"<h2>Transcription job started successfully for S3 object: {object_key}</h2>")
    print("<p>Check AWS Transcribe console for job status and results.</p>")

except Exception as e:
    print("<h2>Error:</h2>")
    print(f"<p>{e}</p>")

