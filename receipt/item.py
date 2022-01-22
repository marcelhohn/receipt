from dataclasses import dataclass
from decimal import Decimal

import receipt.tax_utils as tax_utils

@dataclass()
class Item:
    name: str
    quantity: int
    shelf_price: Decimal
    is_imported: bool

    def calculate_sales_tax(self) -> Decimal:
        tax_rate = self.calculate_tax_rate()
        sales_tax_raw = tax_rate * self.shelf_price
        return tax_utils.round_sales_tax(sales_tax_raw)

    def calculate_tax_rate(self) -> Decimal:
        BASIC_TAX_RATE = Decimal("0.1")
        IMPORT_TAX_RATE = Decimal("0.05")

        tax_rate = Decimal("0")
        if not self.is_basic_tax_free():
            tax_rate += BASIC_TAX_RATE
        if self.is_imported:
            tax_rate += IMPORT_TAX_RATE
        return tax_rate

    def is_basic_tax_free(self) -> bool:
        return any(
            tax_free_good in self.name
            for tax_free_good in ["book", "chocolate", "headache pill"]
        )
