from decimal import Decimal
from unittest import TestCase

from receipt.shopping_basket import ShoppingBasket


class ParseItemInfoFromInputLine(TestCase):
    def test_gets_correct_quantity_for_one_digit_quantity(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line("1 book at 0.00")[0], 1
        )

    def test_gets_correct_quantity_for_two_digit_quantity(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line("42 books at 0.00")[0], 42
        )

    def test_gets_correct_quantity_for_more_than_two_digit_quantity(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line("343 books at 0.00")[0], 343
        )

    def test_gets_correct_description_for_one_word_product(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line("1 book at 0.00")[1], "book"
        )

    def test_gets_correct_description_for_two_word_product(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line("1 music CD at 0.00")[1],
            "music CD",
        )

    def test_gets_correct_description_for_more_than_two_word_product(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line(
                "1 box of imported chocolate at 0.00"
            )[1],
            "box of imported chocolate",
        )

    def test_gets_correct_shelf_price_for_price_below_one(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line("1 book at 0.85")[2],
            Decimal("0.85"),
        )

    def test_gets_correct_shelf_price_for_price_below_ten(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line("1 book at 9.00")[2],
            Decimal("9.00"),
        )

    def test_gets_correct_shelf_price_for_price_above_ten(self):
        self.assertEqual(
            ShoppingBasket.parse_item_info_from_input_line("1 book at 999.99")[2],
            Decimal("999.99"),
        )
