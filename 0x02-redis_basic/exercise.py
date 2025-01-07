#!/usr/bin/env python3
""" exercise file for 0x02 redis basics """

import redis
import uuid


class Cache:
    def __init__(self):
        """intializer"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        """save data in cache"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
