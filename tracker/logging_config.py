import logging
import os
import watchtower

def setup_cloudwatch_logging():
    # Credentials and region should be handled by environment variables
    log_group_name = os.environ.get('AWS_LOG_GROUP_NAME', 'default-health-monitor-log')

    cloudwatch_handler = watchtower.CloudWatchLogHandler(log_group_name)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(cloudwatch_handler)

