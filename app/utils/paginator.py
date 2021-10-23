from typing import List
import math


class Paginator:

    def __init__(self, items: List) -> None:
        self.__items = items
        self.__page_data = {
            "total": len(self.__items),
            "page": 1
        }
        self.__start_index = 0
        self.__end_index = len(self.__items)

    def paginate(self, page: int = 1, limit: int = None):
        self.__page_data["page"] = page

        if limit is not None:
            self.__page_data["pages"] = math.ceil(len(self.__items) / limit)
            self.__page_data["per_page"] = limit
            self.__start_index = (page - 1) * limit
            self.__end_index = self.__start_index + limit

    def get_page_data(self):
        return self.__page_data

    def get_items(self):
        return self.__items[self.__start_index:self.__end_index]
