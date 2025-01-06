#!/usr/bin/env python3
""" search by topic """


def schools_by_topic(mongo_collection, topic):
    """find with a where clause"""
    if mongo_collection is None:
        return []
    return list(mongo_collection.find({"topics": topic}))
