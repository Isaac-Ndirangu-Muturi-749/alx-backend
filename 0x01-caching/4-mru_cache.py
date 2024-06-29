#!/usr/bin/python3
""" Module 4-mru_cache.py """

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache defines a Most Recently Used caching system """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.mru_key = None

    def put(self, key, item):
        """
        Add an item in the cache.
        If the number of items in self.cache_data is higher than
        BaseCaching.MAX_ITEMS, discard the most recently used
        item (MRU algorithm).
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                print(f"DISCARD: {self.mru_key}")
                del self.cache_data[self.mru_key]
            self.cache_data[key] = item

        self.mru_key = key

    def get(self, key):
        """
        Get an item by key from the cache.
        """
        if key is None or key not in self.cache_data:
            return None
        self.mru_key = key
        return self.cache_data[key]
