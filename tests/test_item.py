from dataclasses import FrozenInstanceError
from decimal import Decimal
from unittest import TestCase

from receipt.item import Item


class ItemCreation(TestCase):
    def test_item_is_created_correctly(self):
        test_name = "book"
        test_quantity = 1
        test_shelf_price = Decimal("12.49")
        test_is_imported = False

        test_item = Item(test_name, test_quantity, test_shelf_price, test_is_imported)

        self.assertEqual(test_item.name, test_name)
        self.assertEqual(test_item.quantity, test_quantity)
        self.assertEqual(test_item.shelf_price, test_shelf_price)
        self.assertEqual(test_item.is_imported, test_is_imported)

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
