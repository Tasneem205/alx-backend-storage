#!/usr/bin/env python3
"""insert new collection"""


def insert_school(mongo_collection, **kwargs):
    """insert new collection function"""
    if not mongo_collection:
        return None
    return mongo_collection.insert(kwargs)
