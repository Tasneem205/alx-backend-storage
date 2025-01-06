#!/usr/bin/env python3
""" all """


def list_all(mongo_collection):
    """list all"""
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
