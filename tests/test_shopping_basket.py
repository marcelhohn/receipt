from decimal import Decimal
from unittest import TestCase
from unittest.mock import call, Mock, patch

from receipt.item import Item
from receipt.shopping_basket import ShoppingBasket


class CalculateTotalSalesTaxes(TestCase):
    def test_sums_taxes_correctly(self):
        self.set_up_basket()

        self.assertEqual(
            self.shopping_basket.calculate_total_sales_taxes(), Decimal("2.14")
        )

    def set_up_basket(self) -> None:
        self.set_up_items()
        self.shopping_basket = ShoppingBasket([self.book, self.perfume])

    def set_up_items(self) -> None:
        self.book = Item("book", 1, Decimal("0.00"), False)
        self.perfume = Item("perfume", 1, Decimal("0.00"), False)

        self.book.calculate_sales_tax = Mock(return_value=Decimal("1.15"))
        self.perfume.calculate_sales_tax = Mock(return_value=Decimal("0.99"))


class CalculateTotalPrice(TestCase):
    def test_sums_prices_correctly(self):
        self.set_up_basket()

        self.assertEqual(self.shopping_basket.calculate_total_price(), Decimal("31.14"))

    def set_up_basket(self) -> None:
        self.set_up_items()
        self.shopping_basket = ShoppingBasket([self.book, self.perfume])

    def set_up_items(self) -> None:
        self.book = Item("book", 1, Decimal("0.00"), False)
        self.perfume = Item("perfume", 1, Decimal("0.00"), False)

        self.book.calculate_price_w_sales_tax = Mock(return_value=Decimal("10.15"))
        self.perfume.calculate_price_w_sales_tax = Mock(return_value=Decimal("20.99"))


class Print(TestCase):
    @patch("builtins.print")
    def test_prints_correct_receipt(self, patch_print):
        self.set_up_basket()

        self.shopping_basket.print()

        asserted_calls = [
            call("1 book: 12.49"),
            call("1 imported bottle of perfume: 42.00"),
            call("Sales Taxes: 1.45"),
            call("Total: 54.49"),
        ]
        # We need to check the call count, since assert_has_calls does not check if
        # there have been more calls to the patch before or after the expected calls.
        self.assertEqual(patch_print.call_count, len(asserted_calls))
        patch_print.assert_has_calls(asserted_calls)

    def set_up_basket(self) -> None:
        self.set_up_items()

        self.shopping_basket = ShoppingBasket([self.book, self.perfume])

        self.shopping_basket.calculate_total_sales_taxes = Mock(
            return_value=Decimal("1.45")
        )
        self.shopping_basket.calculate_total_price = Mock(return_value=Decimal("54.49"))

    def set_up_items(self) -> None:
        self.book = Item("book", 1, Decimal("0.00"), False)
        self.perfume = Item("perfume", 1, Decimal("0.00"), False)

        self.book.generate_receipt_text = Mock(return_value="1 book: 12.49")
        self.perfume.generate_receipt_text = Mock(
            return_value="1 imported bottle of perfume: 42.00"
        )
