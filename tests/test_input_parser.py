import pathlib
from decimal import Decimal
from unittest import TestCase

from receipt.input_parser import InputParser


class ParseItemInfoFromInputLine(TestCase):
    def test_gets_correct_quantity_for_one_digit_quantity(self):
        self.assertEqual(self.parse_quantity("1 book at 0.00"), 1)

    def test_gets_correct_quantity_for_two_digit_quantity(self):
        self.assertEqual(self.parse_quantity("42 books at 0.00"), 42)

    def test_gets_correct_quantity_for_more_than_two_digit_quantity(self):
        self.assertEqual(self.parse_quantity("343 books at 0.00"), 343)

    @staticmethod
    def parse_quantity(input: str) -> int:
        return InputParser.parse_item_info_from_input_line(input)[0]

    def test_gets_correct_description_for_one_word_product(self):
        self.assertEqual(self.parse_description("1 book at 0.00"), "book")

    def test_gets_correct_description_for_two_word_product(self):
        self.assertEqual(self.parse_description("1 music CD at 0.00"), "music CD")

    def test_gets_correct_description_for_more_than_two_word_product(self):
        self.assertEqual(
            self.parse_description("1 box of imported chocolate at 0.00"),
            "box of imported chocolate",
        )

    @staticmethod
    def parse_description(input: str) -> str:
        return InputParser.parse_item_info_from_input_line(input)[1]

    def test_gets_correct_shelf_price_for_price_below_one(self):
        self.assertEqual(self.parse_shelf_price("1 book at 0.85"), Decimal("0.85"))

    def test_gets_correct_shelf_price_for_price_below_ten(self):
        self.assertEqual(self.parse_shelf_price("1 book at 9.00"), Decimal("9.00"))

    def test_gets_correct_shelf_price_for_price_above_ten(self):
        self.assertEqual(self.parse_shelf_price("1 book at 999.99"), Decimal("999.99"))

    @staticmethod
    def parse_shelf_price(input: str) -> Decimal:
        return InputParser.parse_item_info_from_input_line(input)[2]


class ParseNameAndOriginFromDescription(TestCase):
    def test_gets_correct_name_for_local_product(self):
        self.assertEqual(self.parse_name("box of chocolate"), "box of chocolate")

    def test_gets_correct_name_for_imported_product(self):
        self.assertEqual(
            self.parse_name("imported box of chocolate"), "box of chocolate"
        )
        self.assertEqual(
            self.parse_name("box of imported chocolate"), "box of chocolate"
        )

    @staticmethod
    def parse_name(description: str) -> str:
        return InputParser.parse_name_and_origin_from_description(description)[0]

    def test_gets_correct_origin_for_local_product(self):
        self.assertEqual(self.parse_is_imported("box of chocolate"), False)

    def test_gets_correct_origin_for_imported_product(self):
        self.assertEqual(self.parse_is_imported("imported box of chocolate"), True)
        self.assertEqual(self.parse_is_imported("box of imported chocolate"), True)

    @staticmethod
    def parse_is_imported(description: str) -> bool:
        return InputParser.parse_name_and_origin_from_description(description)[1]


class ParseItemsFromFile(TestCase):
    def setUp(self) -> None:
        here = pathlib.Path(__file__).parent.resolve()
        self.input_path = here / "test_inputs/input_3.txt"

    def test_creates_correct_list_of_items(self):
        all_output_attributes = InputParser.parse_item_attributes_from_file(
            self.input_path
        )

        all_expected_attributes = [
            ("bottle of perfume", 1, Decimal("27.99"), True),
            ("bottle of perfume", 1, Decimal("18.99"), False),
            ("packet of headache pills", 1, Decimal("9.75"), False),
            ("box of chocolates", 1, Decimal("11.25"), True),
        ]
        for (output_attributes, expected_attributes) in zip(
            all_output_attributes, all_expected_attributes
        ):
            self.assertSequenceEqual(output_attributes, expected_attributes)
