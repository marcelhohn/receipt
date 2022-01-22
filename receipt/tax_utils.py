from decimal import ROUND_UP, Decimal


def round_sales_tax(sales_tax: Decimal) -> Decimal:
    return (sales_tax * 2).quantize(Decimal(".1"), rounding=ROUND_UP) / 2
