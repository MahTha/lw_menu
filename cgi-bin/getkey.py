import boto3

# Configuration
AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
S3_BUCKET_NAME = 'maheshthapa01'

# Initialize S3 client
s3 = boto3.client('s3', region_name=AWS_REGION,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# List objects in the bucket
try:
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)

    if 'Contents' in response:
        print(f"Objects in bucket '{S3_BUCKET_NAME}':")
        for obj in response['Contents']:
            print(f"- {obj['Key']}")

    else:
        print(f"No objects found in bucket '{S3_BUCKET_NAME}'.")

except Exception as e:
    print(f"Error listing objects in bucket '{S3_BUCKET_NAME}': {e}")

