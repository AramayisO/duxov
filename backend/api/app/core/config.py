from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")


class AppConfig:
    
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", cast=Secret, default=None)
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=Secret, default=None)
    AWS_DEFAULT_REGION = config("AWS_DEFAULT_REGION", cast=str, default="")
