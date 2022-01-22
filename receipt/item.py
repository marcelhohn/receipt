from dataclasses import dataclass
from decimal import Decimal


@dataclass()
class Item:
    name: str
    quantity: int
    shelf_price: Decimal
    is_imported: bool

    def calculate_sales_tax(self) -> Decimal:
        self.calculate_tax_rate()
        return Decimal("0.0")

    def calculate_tax_rate(self) -> Decimal:
        self.is_basic_tax_free()
        return Decimal("0.0")

    def is_basic_tax_free(self) -> bool:
        return any(
            tax_free_good in self.name
            for tax_free_good in ["book", "chocolate", "headache pill"]
        )
