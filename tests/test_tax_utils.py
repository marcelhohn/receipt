from decimal import Decimal
from unittest import TestCase

import receipt.tax_utils as tax_utils


class RoundSalesTax(TestCase):
    def test_rounds_up_correctly(self):
        self.assertEqual(tax_utils.round_sales_tax(Decimal("0.0501")), Decimal("0.10"))
        self.assertEqual(tax_utils.round_sales_tax(Decimal("1.43")), Decimal("1.45"))

    def test_does_not_change_if_tax_is_multiple_of_rounding_step(self):
        self.assertEqual(tax_utils.round_sales_tax(Decimal("0.05")), Decimal("0.05"))
        self.assertEqual(tax_utils.round_sales_tax(Decimal("0.1000")), Decimal("0.10"))

    def test_returns_numbers_with_two_decimals(self):
        result_decimals = -tax_utils.round_sales_tax(Decimal("0.2")).as_tuple().exponent
        self.assertEqual(2, result_decimals)
