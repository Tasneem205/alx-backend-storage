#!/usr/bin/env python3
""" change topics """


def update_topics(mongo_collection, name, topics):
    """change topics function """
    if mongo_collection is None:
        return
    mongo_collection.update_many({"name": name}, {$set: {"topics": topics}})
