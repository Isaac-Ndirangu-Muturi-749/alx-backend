#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Deletion-resilient hypermedia pagination"""
        assert index is not None and index >= 0
        assert page_size > 0

        indexed_dataset = self.indexed_dataset()
        dataset_size = len(indexed_dataset)

        assert index < dataset_size

        data = []
        next_index = index

        while len(data) < page_size and next_index < dataset_size:
            item = indexed_dataset.get(next_index, None)
            if item is not None:
                data.append(item)
            next_index += 1

        return {
            'index': index,
            'next_index': next_index if next_index < dataset_size else None,
            'page_size': len(data),
            'data': data
        }
