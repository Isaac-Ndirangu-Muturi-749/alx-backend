#!/usr/bin/python3
""" Module 100-lfu_cache.py """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache defines a Least Frequently Used caching system """

    def __init__(self):
        """ Initialize the cache """
        super().__init__()
        self.usage_counts = {}
        self.lru_order = {}

    def put(self, key, item):
        """
        Add an item in the cache.
        If the number of items in self.cache_data is higher than
        BaseCaching.MAX_ITEMS,
        discard the least frequency used item (LFU algorithm).
        If there is a tie, discard the least recently used item.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.usage_counts[key] += 1
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lfu_key = min(
                    self.usage_counts,
                    key=lambda k: (self.usage_counts[k], self.lru_order[k]))

                print(f"DISCARD: {lfu_key}")
                del self.cache_data[lfu_key]
                del self.usage_counts[lfu_key]
                del self.lru_order[lfu_key]

            self.cache_data[key] = item
            self.usage_counts[key] = 1

        self.lru_order[key] = max(self.lru_order.values(), default=0) + 1

    def get(self, key):
        """
        Get an item by key from the cache.
        """
        if key is None or key not in self.cache_data:
            return None

        self.usage_counts[key] += 1
        self.lru_order[key] = max(self.lru_order.values(), default=0) + 1
        return self.cache_data[key]
