from starlette.datastructures import Secret

from app.core.config import AppConfig


def test_has_aws_config():
    """
    Test that the global config object has the necessary AWS API config vars.
    """
    assert AppConfig.AWS_ACCESS_KEY_ID is not None
    assert AppConfig.AWS_SECRET_ACCESS_KEY is not None
    assert AppConfig.AWS_DEFAULT_REGION is not None


def test_aws_keys_are_secret():
    """
    Test that the AWS access key and secret key are wrapped in Starlette's
    Secret object to prevent the values from being unintentionally printed
    out to the console or in logs.
    """
    assert type(AppConfig.AWS_ACCESS_KEY_ID) == Secret
    assert type(AppConfig.AWS_SECRET_ACCESS_KEY) == Secret
