from decimal import ROUND_UP, Decimal

from receipt.item import Item


def calculate_sales_tax(item: Item) -> Decimal:
    calculate_tax_rate(item)
    return Decimal('0.0')

def calculate_tax_rate(item: Item) -> Decimal:
    is_basic_tax_free(item)
    return Decimal('0.0')

def is_basic_tax_free(item: Item) -> bool:
    return False

def round_sales_tax(sales_tax: Decimal) -> Decimal:
    return (sales_tax * 2).quantize(Decimal('.1'), rounding=ROUND_UP) / 2