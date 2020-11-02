import io

import pytest

from app.storage.service import StorageService

TEST_FILE_PATH = "test.txt"
TEST_FILE_CONTENT = "This is a test file.\n"


def test_get_byte_stream_success(storage: StorageService):
    """
    Test that the StorageService successfully returns an io.BytesIO stream with
    the correct file content if the file exists.
    """
    stream = storage.get_byte_stream(TEST_FILE_PATH)
    
    assert stream is not None
    assert type(stream) is io.BytesIO

    # Make sure we're reading from the start of the stream
    stream.seek(0)
    assert stream.read().decode('utf-8') == TEST_FILE_CONTENT


def test_get_byte_stream_error(storage: StorageService):
    """
    Test that the StorageService raises a FileNotFoundError if the specified
    file was not found.
    """
    with pytest.raises(FileNotFoundError):
        storage.get_byte_stream("")


def test_get_string_stream_success(storage: StorageService):
    """
    Test that the StorageService successfully returns an io.StringIO stream
    with the correct file content if the file exists.
    """
    stream = storage.get_string_stream(TEST_FILE_PATH)

    assert stream is not None
    assert type(stream) == io.StringIO

    # Make sure we're reading from the start of the stream
    stream.seek(0)
    assert stream.read() == TEST_FILE_CONTENT


def test_get_string_stream_error(storage: StorageService):
    """
    Test that the StorageService raises a FileNotFoundError if the specified
    file was not found.
    """
    with pytest.raises(FileNotFoundError):
        storage.get_string_stream("")
