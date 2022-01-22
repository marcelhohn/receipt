from decimal import Decimal
from unittest import TestCase
from unittest.mock import call, Mock, patch

from receipt.item import Item
from receipt.shopping_basket import ShoppingBasket

class TotalSalesTaxesCalculation(TestCase):
    def test_calculates_total_sales_taxes_correctly(self):
        book = Item("book", 1, Decimal("0.00"), False)
        perfume = Item("perfume", 1, Decimal("0.00"), False)
        shopping_basket = ShoppingBasket([book, perfume])

        book.calculate_sales_tax = Mock(return_value=Decimal("1.15"))
        perfume.calculate_sales_tax = Mock(return_value=Decimal("0.99"))

        self.assertEqual(shopping_basket.calculate_total_sales_taxes(), Decimal("2.14"))

class TotalPriceCalculation(TestCase):
    def test_calculates_total_sales_taxes_correctly(self):
        book = Item("book", 1, Decimal("0.00"), False)
        perfume = Item("perfume", 1, Decimal("0.00"), False)
        shopping_basket = ShoppingBasket([book, perfume])

        book.calculate_price_w_sales_tax = Mock(return_value=Decimal("10.15"))
        perfume.calculate_price_w_sales_tax = Mock(return_value=Decimal("20.99"))

        self.assertEqual(shopping_basket.calculate_total_price(), Decimal("31.14"))


class Printing(TestCase):
    @patch('builtins.print')
    def test_print_correct_receipt(self, patch_print):
        book = Item("book", 1, Decimal("0.00"), False)
        perfume = Item("perfume", 1, Decimal("0.00"), False)
        shopping_basket = ShoppingBasket([book, perfume])

        book.generate_receipt_text = Mock(return_value="1 book: 12.49")
        perfume.generate_receipt_text = Mock(return_value="1 imported bottle of perfume: 42.00")
        shopping_basket.calculate_total_sales_taxes = Mock(return_value=Decimal("1.45"))
        shopping_basket.calculate_total_price = Mock(return_value=Decimal("54.49"))


        shopping_basket.print()
        self.assertEqual(patch_print.call_count, 4)
        patch_print.assert_has_calls([
            call("1 book: 12.49"),
            call("1 imported bottle of perfume: 42.00"),
            call("Sales Taxes: 1.45"),
            call("Total: 54.49")
        ])