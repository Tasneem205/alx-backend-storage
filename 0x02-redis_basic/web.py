#!/usr/bin/env python3
"""advanced exercise file for 0x02 redis basics """

import redis
import requests
from functools import wraps
from typing import Callable


redis_client = redis.Redis()


def track_url_access(method: Callable) -> Callable:
    """ rtack url access function """
    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        cache_key = f"cache:{url}"
        cached_page = redis_client.get(cache_key)
        if cached_page:
            return cached_page.decode("utf-8")
        response = method(url)
        redis_client.setex(cache_key, 10, response)
        return response
    return wrapper


@track_url_access
def get_page(url: str) -> str:
    """get page function"""
    response = requests.get(url)
    return response.text
