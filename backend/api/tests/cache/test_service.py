import pytest
import uuid

from app.cache.service import CacheService

def test_key_value_correct_type(cache: CacheService):
    """
    Test that a key-value pair is successfully added to the cache and
    retrieved from the cache.
    """
    # Using a random UUID should guarnatee that the key is unique each time
    # the test is run, even if the cache isn't cleared.
    key = str(uuid.uuid4())
    value = "some value"

    # Make sure key does not exist before test
    assert cache.get(key) == None

    # Add the key-value pair and check that it was actuially added.
    assert cache.set(key, value) == True
    assert cache.get(key) == value.encode('utf-8')


def test_type_error(cache: CacheService):
    """
    Test that the cache raises an error if the provided key or value have
    the wrong type.
    """
    # Invalid type for key
    with pytest.raises(TypeError):
        cache.set(["key"], "value")

    # Invalid type for value
    with pytest.raises(TypeError):
        cache.set("key", ["value"])

    # Invalid type for key
    with pytest.raises(TypeError):
        cache.get(["key"])

    # Invalid type for key
    with pytest.raises(TypeError):
        cache.clear(["key"])


def test_clear_keys(cache: CacheService):
    key = str(uuid.uuid4())

    # Should return 0 since the key was not added to the cache
    assert cache.clear(key) == 0

    cache.set(key, "")

    # Should return 1 since the key was added to the cache.
    assert cache.clear(key) == 1

    keys = [str(uuid.uuid4()) for i in range(3)]
    for key in keys: 
        cache.set(key, "")

    # Should return 3 since all 3 keys were added to the cache.
    assert cache.clear(*keys) == 3

    keys = [str(uuid.uuid4()) for i in range(3)]
    for key in keys[:2]: 
        cache.set(key, "")

    # Should return 2 since only 2 of the keys were added.
    assert cache.clear(*keys) == 2
