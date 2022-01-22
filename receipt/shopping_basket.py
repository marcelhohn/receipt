from decimal import Decimal
from typing import List

from receipt.item import Item

class ShoppingBasket:
    def __init__(self) -> None:
        self._items = []

    def add(self, items: List[Item]) -> None:
        return

    def print(self) -> None:
        print()

    def calculate_total_sales_taxes(self) -> Decimal:
        return Decimal("0.00")

    def calculate_total_price(self) -> Decimal:
        return Decimal("0.00")