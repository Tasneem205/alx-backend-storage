#!/usr/bin/env python3
""" exercise file for 0x02 redis basics """

import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def replay(method: Callable) -> None:
    """ reply """
    redis_instance = method.__self__._redis
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    call_count = len(inputs)
    print(f"{method.__qualname__} was called {call_count} times:")
    for input_args, output in zip(inputs, outputs):
        decoded_input = input_args.decode('utf-8')  # Decode the input
        decoded_output = output.decode('utf-8')    # Decode the output
        print(f"{method.__qualname__}(*{decoded_input}) -> {decoded_output}")


def call_history(method: Callable) -> Callable:
    """ call history """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ INCR function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    cache class 
    """
    def __init__(self):
        """intializer"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """save data in cache"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """get key"""
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """get value as result"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """get value as result"""
        return self.get(key, fn=int)
