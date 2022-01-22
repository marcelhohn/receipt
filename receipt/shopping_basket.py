from decimal import Decimal
from typing import List

from receipt.item import Item

class ShoppingBasket:
    def __init__(self, items: List[Item]) -> None:
        self._items = items

    def print(self) -> None:
        for item in self._items:
            print(item.generate_receipt_text())
        
        total_sales_taxes = self.calculate_total_sales_taxes()
        print(f"Sales Taxes: {total_sales_taxes}")
        
        total_price = self.calculate_total_price()
        print(f"Total: {total_price}")

    def calculate_total_sales_taxes(self) -> Decimal:
        return sum([item.calculate_sales_tax() for item in self._items])

    def calculate_total_price(self) -> Decimal:
        return sum([item.calculate_price_w_sales_tax() for item in self._items])

        