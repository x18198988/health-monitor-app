import boto3
from django.conf import settings

def send_sns_email_notification(subject, message):
    sns = boto3.client(
        'sns',
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    
    response = sns.publish(
        TopicArn=settings.AWS_SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )
    
    return response
