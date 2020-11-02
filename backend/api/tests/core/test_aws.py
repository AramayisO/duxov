from app.core.aws import session


def test_aws_session_not_none():
    """
    Test that the AWS session object is not None.
    """
    assert session is not None
