from typing import Union, Text

import redis

from app.core.config import AppConfig
from app.cache.models import Key, Value


class CacheService:
    
    __redis = redis.Redis(host=AppConfig.REDIS_HOST, port=AppConfig.REDIS_PORT)


    @classmethod
    def set(cls, key: Key, value: Value) -> bool:
        """Sets the value at the key `key` to `value`.

        Args:
            key (app.cache.models.Key): The key for which to set the value.
            value (app.cache.models.Value): The value to set for the key.

        Returns:
            bool: True if the value was successfully set, False otherwise.
        
        Raises:
            TypeError: The provided key or value have the wrong type.
        """
        try:
            result = cls.__redis.set(key, value)
        except redis.exceptions.DataError as error:
            raise TypeError(error)
        return result


    @classmethod
    def get(cls, key: Key) -> Union[bytes, None]:
        """Get the value for the specified key.

        Args:
            key (app.cache.models.Key):

        Returns:
            bytes: The value set for key or None if the key is not set.

        Raises:
            TypeError: The specified key is of the wrong type.
        """
        try:
            value = cls.__redis.get(key)
        except redis.exceptions.DataError as error:
            raise TypeError(error)
        return value


    @classmethod
    def clear(cls, *keys: Key) -> int:
        """Delete values set for the specified keys.

        Args:
            keys (app.cache.models.Key): The keys to be deleted.

        Returns:
            int: The number of keys deleted.

        Raises:
            TypeError: At least one key has the wrong type.
        """
        try:
            result = cls.__redis.delete(*keys)
        except redis.exceptions.DataError as error:
            raise TypeError(error)
        return result