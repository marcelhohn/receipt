from dataclasses import FrozenInstanceError
from decimal import Decimal
from unittest import TestCase
import unittest
from unittest.mock import Mock, patch

from receipt.item import Item


class ItemCreation(TestCase):
    def test_item_is_created_correctly(self):
        test_name = "book"
        test_quantity = 1
        test_shelf_price = Decimal("12.49")
        test_is_imported = False

        test_item = Item(test_name, test_quantity, test_shelf_price, test_is_imported)

        self.assertEqual(test_item._name, test_name)
        self.assertEqual(test_item._quantity, test_quantity)
        self.assertEqual(test_item._shelf_price, test_shelf_price)
        self.assertEqual(test_item._is_imported, test_is_imported)

    @unittest.skip(
        "unfreeze dataclass since frozen dataclass does not allow to mock mehtods, "
        "which we need for testing other mehtods of the Item class"
    )
    def test_item_does_not_allow_mutation_after_creation(self):
        test_name = "book"
        test_quantity = 1
        test_shelf_price = Decimal("12.49")
        test_is_imported = False

        test_item = Item(test_name, test_quantity, test_shelf_price, test_is_imported)

        with self.assertRaises(FrozenInstanceError):
            test_item.name = "CD"
        with self.assertRaises(FrozenInstanceError):
            test_item.quantity = 2
        with self.assertRaises(FrozenInstanceError):
            test_item.shelf_price = Decimal("0.49")
        with self.assertRaises(FrozenInstanceError):
            test_item.is_imported = True


class BasicTaxFreeCheck(TestCase):
    def test_book_is_basic_tax_free(self):
        book = Item("book", 1, Decimal("0.00"), False)
        self.assertTrue(book.is_basic_tax_free())

    def test_chocolate_bar_is_basic_tax_free(self):
        chocolate_bar = Item("chocolate_bar", 1, Decimal("0.00"), False)
        self.assertTrue(chocolate_bar.is_basic_tax_free())

    def test_box_of_chocolates_is_basic_tax_free(self):
        box_of_chocolates = Item("box of chocolates", 1, Decimal("0.00"), False)
        self.assertTrue(box_of_chocolates.is_basic_tax_free())

    def test_packet_of_headache_pills_is_basic_tax_free(self):
        packet_of_headache_pills = Item(
            "packet of headache pills", 1, Decimal("0.00"), False
        )
        self.assertTrue(packet_of_headache_pills.is_basic_tax_free())

    def test_music_CD_is_not_basic_tax_free(self):
        music_cd = Item("music CD", 1, Decimal("0.00"), False)
        self.assertFalse(music_cd.is_basic_tax_free())

    def bottle_of_prefume_is_not_basic_tax_free(self):
        bottle_of_perfume = Item("bottle of perfume", 1, Decimal("0.00"), False)
        self.assertFalse(bottle_of_perfume.is_basic_tax_free())


class TaxRateCalculation(TestCase):
    def test_tax_rate_for_essential_item(self):
        essential_item = Item("", 1, Decimal("0.00"), False)
        essential_item.is_basic_tax_free = Mock(return_value=True)

        self.assertEqual(essential_item.calculate_tax_rate(), Decimal("0"))

    def test_tax_rate_for_normal_item(self):
        normal_item = Item("", 1, Decimal("0.00"), False)
        normal_item.is_basic_tax_free = Mock(return_value=False)

        self.assertEqual(normal_item.calculate_tax_rate(), Decimal("0.1"))

    def test_tax_rate_for_imported_essential_item(self):
        imported_essential_item = Item("", 1, Decimal("0.00"), True)
        imported_essential_item.is_basic_tax_free = Mock(return_value=True)

        self.assertEqual(imported_essential_item.calculate_tax_rate(), Decimal("0.05"))

    def test_tax_rate_for_imported_normal_item(self):
        imported_normal_item = Item("", 1, Decimal("0.00"), True)
        imported_normal_item.is_basic_tax_free = Mock(return_value=False)

        self.assertEqual(imported_normal_item.calculate_tax_rate(), Decimal("0.15"))


class SalesTaxCalculation(TestCase):
    @patch("receipt.item.tax_utils.round_sales_tax")
    def test_round_sales_tax_is_called_with_no_tax(self, patch_round_sales_tax):
        item = Item("", 1, Decimal("12.49"), False)
        item.calculate_tax_rate = Mock(return_value=Decimal("0"))

        item.calculate_sales_tax()
        patch_round_sales_tax.assert_called_once_with(Decimal("0"))

    @patch("receipt.item.tax_utils.round_sales_tax")
    def test_round_sales_tax_called_is_called_with_correct_raw_sales_tax(
        self, patch_round_sales_tax
    ):
        item = Item("", 1, Decimal("12.49"), False)
        item.calculate_tax_rate = Mock(return_value=Decimal("0.15"))

        item.calculate_sales_tax()
        patch_round_sales_tax.assert_called_once_with(Decimal("1.8735"))


class PriceWithSalesTaxCalculation(TestCase):
    def test_unimported_essential_items(self):
        self.assertEqual(
            Item("book", 1, Decimal("12.49"), False).calculate_price_w_sales_tax(),
            Decimal("12.49"),
        )
        self.assertEqual(
            Item(
                "chocolate bar", 1, Decimal("0.85"), False
            ).calculate_price_w_sales_tax(),
            Decimal("0.85"),
        )
        self.assertEqual(
            Item(
                "packet of headache pills", 1, Decimal("9.75"), False
            ).calculate_price_w_sales_tax(),
            Decimal("9.75"),
        )

    def test_unimported_normal_items(self):
        self.assertEqual(
            Item("music CD", 1, Decimal("14.99"), False).calculate_price_w_sales_tax(),
            Decimal("16.49"),
        )
        self.assertEqual(
            Item(
                "bottle of perfume", 1, Decimal("18.99"), False
            ).calculate_price_w_sales_tax(),
            Decimal("20.89"),
        )

    def test_imported_essential_items(self):
        self.assertEqual(
            Item(
                "box of chocolates", 1, Decimal("10.00"), True
            ).calculate_price_w_sales_tax(),
            Decimal("10.50"),
        )
        self.assertEqual(
            Item(
                "box of chocolates", 1, Decimal("11.25"), True
            ).calculate_price_w_sales_tax(),
            Decimal("11.85"),
        )

    def test_imported_normal_items(self):
        self.assertEqual(
            Item(
                "bottle of perfume", 1, Decimal("47.50"), True
            ).calculate_price_w_sales_tax(),
            Decimal("54.65"),
        )
        self.assertEqual(
            Item(
                "bottle of perfume", 1, Decimal("27.99"), True
            ).calculate_price_w_sales_tax(),
            Decimal("32.19"),
        )
