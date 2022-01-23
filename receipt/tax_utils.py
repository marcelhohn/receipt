from decimal import ROUND_UP, Decimal


def round_sales_tax(sales_tax: Decimal) -> Decimal:
    rounded_sales_tax = (sales_tax * 2).quantize(Decimal(".1"), rounding=ROUND_UP) / 2
    return rounded_sales_tax.quantize(Decimal(".01"))
