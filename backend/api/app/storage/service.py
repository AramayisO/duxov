import io

from app.core.config import AppConfig
from app.core.aws import session


class StorageService(object):

    __s3 = session.resource("s3")
    __bucket = __s3.Bucket(AppConfig.S3_BUCKET_NAME)

    @classmethod
    def get_byte_stream(cls, filepath: str) -> io.BytesIO:
        """Reads a file from storage and returns the data as a byte stream.

        Args:
            filepath (str): The path to the file to be read.

        Returns:
            io.BytesIO: The content of the specified file.

        Raises:
            FileNotFoundError: The specified file was not found.
        """
        byte_stream = io.BytesIO()

        # Read file from S3 bucket as a binary byte stream.
        try:
            cls.__bucket.download_fileobj(filepath, byte_stream)
        except:
            raise FileNotFoundError(
                f"'{filepath}' not found in the '{cls.__bucket.name}' bucket"
            )

        # Set read position back to the start of the stream after write.
        byte_stream.seek(0)
        
        return byte_stream


    @classmethod
    def get_string_stream(cls, filepath: str) -> io.StringIO:
        """Reads a file from storage and returns the data as a string stream.

        Args:
            filepath (str): The path to the file to be read.

        Returns:
            io.StringIO: The content of the specified file.

        Raises:
            FileNotFoundError: The specified file was not found.
        """
        byte_stream = cls.get_byte_stream(filepath)

        # Convert the byte stream into a string stream.
        string_stream = io.StringIO(byte_stream.read().decode('utf-8'))
        
         # Set read position back to the start of the stream after write.
        string_stream.seek(0)

        return string_stream
