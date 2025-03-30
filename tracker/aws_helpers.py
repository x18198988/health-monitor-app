import boto3
from django.conf import settings

def upload_file_to_s3(local_file_path, s3_key):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        s3.upload_file(local_file_path, settings.AWS_STORAGE_BUCKET_NAME, s3_key)
        print(f"✅ Uploaded {local_file_path} to S3 as {s3_key}")
        return True
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")
        return False
