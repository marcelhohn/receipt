from decimal import Decimal
from typing import Tuple
import re

from receipt.item import Item


class ShoppingBasket:
    def __init__(self) -> None:
        self._items = []

    @staticmethod
    def parse_item_info_from_input_line(input_line: str) -> Tuple[int, str, Decimal]:
        quantity_and_description, shelf_price_text = input_line.split(" at ")
        
        shelf_price = Decimal(shelf_price_text)
        
        PATTERN_TEXT = r"(?P<quantity>\d+) (?P<description>[\w\s]+)"
        pattern = re.compile(PATTERN_TEXT)
        match = pattern.match(quantity_and_description)
        quantity = int(match.group("quantity"))
        description = match.group("description")

        return quantity, description, shelf_price

    @staticmethod
    def parse_name_and_origin_from_description(description) -> Tuple[str, bool]:
        if "imported" in description:
            name = " ".join(description.replace("imported", "").split())
            return name, True
        else:
            return description, False

    def add_item(self, item: Item) -> None:
        return
