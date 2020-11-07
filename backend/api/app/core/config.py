from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


class AppConfig:
    # AWS account config
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", cast=Secret, default=None)
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=Secret, default=None)
    AWS_DEFAULT_REGION = config("AWS_DEFAULT_REGION", cast=str, default="")
    
    # S3 storage config
    S3_BUCKET_NAME = config("S3_BUCKET_NAME", cast=str, default=None)

    # Redis cache config
    REDIS_HOST = config("REDIS_HOST", cast=str, default="127.0.0.1")
    REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
