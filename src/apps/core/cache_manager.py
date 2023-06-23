from django.core.cache import cache


# This function set value
def set_key(key, value, timeout=None):
    return cache.set(key, value, timeout=timeout)


# this function gets value by key
def get_value_by_key(key):
    return cache.get(key)


# this function deletes value by key
def delete_key(key):
    return cache.delete(key)


# this function deletes value by pattern
def get_keys(pattern):
    return cache.keys(pattern)
