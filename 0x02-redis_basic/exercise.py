#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of the
Redis client as a private variable named _redis (using redis.Redis())
and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the
input data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a
str, bytes, int or float.
"""
import redis
from typing import Union, Any, Callable
from uuid import uuid4
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    decorator to store the history of inputs and outputs
    for a particular function
    """
    @wraps(method)
    def wrapper_call(self, *args, **kwargs):
        """wrapperfunc"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        out = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(out))
        return out
    return wrapper_call


def count_calls(method: Callable) -> Callable:
    """count the no of times a method is called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper_count(self, *args, **kwargs):
        """wrapper function"""
        self._redis.incr(key, amount=1)
        return method(self, *args, **kwargs)
    return wrapper_count


class Cache:
    """cache class"""
    def __init__(self):
        """instance intialization"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generates a rndom key and then uses this key to
        store the data argument into redis database
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Any:
        """
        get method that take a key string argument and an optional Callable
        argument named fn. This callable will be used to convert the data
        back to the desired format
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """return str"""
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """retrun int"""
        value = self._redis.get(key)
        return int.from_bytes(value)


def replay(fn: Callable):
    """display the history of calls of a particular function."""
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""
        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""
        print("{}(*{}) -> {}".format(func_name, input, output))
