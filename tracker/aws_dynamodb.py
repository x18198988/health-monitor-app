import boto3
from django.conf import settings
from datetime import datetime

def log_to_dynamodb(username, steps, sleep_hours, calories):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=settings.AWS_S3_REGION_NAME,  # same as your S3 region
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    table = dynamodb.Table('x18198988-HealthDataSummary')

    response = table.put_item(
        Item={
            'username': username,
            'timestamp': datetime.utcnow().isoformat(),
            'summary': f"Steps: {steps}, Sleep: {sleep_hours} hrs, Calories: {calories}"
        }
    )

    return response
