from dataclasses import dataclass
from decimal import Decimal
import receipt

import receipt.tax_utils as tax_utils


@dataclass()
class Item:
    _name: str
    _quantity: int
    _shelf_price: Decimal
    _is_imported: bool

    def calculate_price_w_sales_tax(self) -> Decimal:
        return self._shelf_price + self.calculate_sales_tax()

    def calculate_sales_tax(self) -> Decimal:
        tax_rate = self.calculate_tax_rate()
        sales_tax_raw = tax_rate * self._shelf_price
        return tax_utils.round_sales_tax(sales_tax_raw)

    def calculate_tax_rate(self) -> Decimal:
        BASIC_TAX_RATE = Decimal("0.1")
        IMPORT_TAX_RATE = Decimal("0.05")

        tax_rate = Decimal("0")
        if not self.is_basic_tax_free():
            tax_rate += BASIC_TAX_RATE
        if self._is_imported:
            tax_rate += IMPORT_TAX_RATE
        return tax_rate

    def is_basic_tax_free(self) -> bool:
        TAX_FREE_GOODS = ["book", "chocolate", "headache pill"]

        return any(tax_free_good in self._name for tax_free_good in TAX_FREE_GOODS)

    def generate_receipt_text(self) -> str:
        return f"{self._quantity} {'imported ' if self._is_imported else ''}{self._name}: {self.calculate_price_w_sales_tax()}"
