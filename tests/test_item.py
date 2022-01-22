from dataclasses import FrozenInstanceError
from decimal import Decimal
from unittest import TestCase

from receipt.item import Item

class ItemTestCase(TestCase):

    def test_item_is_created_correctly(self):
        test_name = "book"
        test_quantity = 1
        test_shelf_price = Decimal('12.49')
        test_is_imported = False

        test_item = Item(test_name, test_quantity, test_shelf_price, test_is_imported)
        
        self.assertEqual(test_item.name, test_name)
        self.assertEqual(test_item.quantity, test_quantity)
        self.assertEqual(test_item.shelf_price, test_shelf_price)
        self.assertEqual(test_item.is_imported, test_is_imported)

    def test_item_does_not_allow_mutation_after_creation(self):
        test_name = "book"
        test_quantity = 1
        test_shelf_price = Decimal('12.49')
        test_is_imported = False

        test_item = Item(test_name, test_quantity, test_shelf_price, test_is_imported)

        with self.assertRaises(FrozenInstanceError):
            test_item.name = "CD"
        with self.assertRaises(FrozenInstanceError):
            test_item.quantity = 2
        with self.assertRaises(FrozenInstanceError):
            test_item.shelf_price = Decimal('0.49')
        with self.assertRaises(FrozenInstanceError):
            test_item.is_imported = True
