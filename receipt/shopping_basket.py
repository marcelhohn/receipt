from decimal import Decimal
from typing import Tuple

from receipt.item import Item


class ShoppingBasket:
    def __init__(self) -> None:
        self._items = []

    def parse_item_info_from_input_line(
        self, input_line: str
    ) -> Tuple[int, str, Decimal]:
        return 0, "", Decimal("0")

    def check_if_item_imported(self, item_name_w_origin) -> bool:
        return False

    def add_item(self, item: Item) -> None:
        return
