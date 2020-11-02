import boto3

from app.core.config import AppConfig

session = boto3.Session(
    aws_access_key_id=str(AppConfig.AWS_ACCESS_KEY_ID),
    aws_secret_access_key=str(AppConfig.AWS_SECRET_ACCESS_KEY),
    region_name=AppConfig.AWS_DEFAULT_REGION
)