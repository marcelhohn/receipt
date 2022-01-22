from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Item:
   name: str
   quantity: int
   shelf_price: Decimal
   is_imported: bool 