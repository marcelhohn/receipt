from decimal import Decimal
from unittest import TestCase
from unittest.mock import Mock, patch

from receipt.item import Item


class Init(TestCase):
    def test_creates_item_correctly(self):
        test_name = "book"
        test_quantity = 1
        test_shelf_price = Decimal("12.49")
        test_is_imported = False

        test_item = Item(test_name, test_quantity, test_shelf_price, test_is_imported)

        self.assertEqual(test_item._name, test_name)
        self.assertEqual(test_item._quantity, test_quantity)
        self.assertEqual(test_item._shelf_price, test_shelf_price)
        self.assertEqual(test_item._is_imported, test_is_imported)


class IsBasicTaxFree(TestCase):
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


class CalculateTaxRate(TestCase):
    def test_works_for_essential_item(self):
        essential_item = self.create_item(is_essential=True, is_imported=False)

        self.assertEqual(essential_item.calculate_tax_rate(), Decimal("0"))

    def test_works_for_normal_item(self):
        normal_item = self.create_item(is_essential=False, is_imported=False)

        self.assertEqual(normal_item.calculate_tax_rate(), Decimal("0.1"))

    def test_works_for_imported_essential_item(self):
        imported_essential_item = self.create_item(is_essential=True, is_imported=True)

        self.assertEqual(imported_essential_item.calculate_tax_rate(), Decimal("0.05"))

    def test_works_for_imported_normal_item(self):
        imported_normal_item = self.create_item(is_essential=False, is_imported=True)

        self.assertEqual(imported_normal_item.calculate_tax_rate(), Decimal("0.15"))

    @staticmethod
    def create_item(is_essential: bool, is_imported: bool) -> Item:
        item = Item("", 1, Decimal("0.00"), is_imported)
        item.is_basic_tax_free = Mock(return_value=is_essential)
        return item


class CalculateSalesTax(TestCase):
    @patch("receipt.item.tax_utils.round_sales_tax")
    def test_calls_round_sales_tax_with_no_tax(self, patch_round_sales_tax):
        item = Item("", 1, Decimal("12.49"), False)
        item.calculate_tax_rate = Mock(return_value=Decimal("0"))

        item.calculate_sales_tax()
        patch_round_sales_tax.assert_called_once_with(Decimal("0"))

    @patch("receipt.item.tax_utils.round_sales_tax")
    def test_calls_round_sales_tax_with_correct_raw_sales_tax(
        self, patch_round_sales_tax
    ):
        item = Item("", 1, Decimal("12.49"), False)
        item.calculate_tax_rate = Mock(return_value=Decimal("0.15"))

        item.calculate_sales_tax()
        patch_round_sales_tax.assert_called_once_with(Decimal("1.8735"))


class CalcualtePriceWithSalesTax(TestCase):
    def test_works_for_unimported_essential_items(self):
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

    def test_works_for_unimported_normal_items(self):
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

    def test_works_for_imported_essential_items(self):
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

    def test_works_for_imported_normal_items(self):
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


class GenerateReceiptText(TestCase):
    def test_works_for_local_good(self):
        item = Item("bottle of perfume", 1, Decimal("0.00"), False)
        item.calculate_price_w_sales_tax = Mock(return_value=Decimal("42.00"))

        self.assertEqual(item.generate_receipt_text(), "1 bottle of perfume: 42.00")

    def test_works_for_imported_good(self):
        item = Item("box of chocolates", 1, Decimal("0.00"), True)
        item.calculate_price_w_sales_tax = Mock(return_value=Decimal("0.99"))

        self.assertEqual(
            item.generate_receipt_text(), "1 imported box of chocolates: 0.99"
        )
