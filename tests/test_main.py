import pathlib
from unittest import TestCase
from unittest.mock import call, patch

from receipt.main import print_receipt



class PrintReceipt(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.here = pathlib.Path(__file__).parent.resolve()

    @patch('builtins.print')
    def test_print_correct_receipt_input_1(self, patch_print):
        path_to_input_1 = str(self.here / "test_inputs/input_1.txt")
        
        print_receipt(path_to_input_1)

        expected_calls = [
                call("1 book: 12.49"),
                call("1 music CD: 16.49"),
                call("1 chocolate bar: 0.85"),
                call("Sales Taxes: 1.50"),
                call("Total: 29.83"),
            ]
        self.assertSequenceEqual(expected_calls, patch_print.call_args_list)

    @patch('builtins.print')
    def test_print_correct_receipt_input_2(self, patch_print):
        path_to_input_1 = str(self.here / "test_inputs/input_2.txt")
        
        print_receipt(path_to_input_1)

        expected_calls = [
                call("1 imported box of chocolates: 10.50"),
                call("1 imported bottle of perfume: 54.65"),
                call("Sales Taxes: 7.65"),
                call("Total: 65.15"),
            ]
        self.assertSequenceEqual(expected_calls, patch_print.call_args_list)

    @patch('builtins.print')
    def test_print_correct_receipt_input_3(self, patch_print):
        path_to_input_1 = str(self.here / "test_inputs/input_3.txt")
        
        print_receipt(path_to_input_1)

        expected_calls = [
                call("1 imported bottle of perfume: 32.19"),
                call("1 bottle of perfume: 20.89"),
                call("1 packet of headache pills: 9.75"),
                call("1 imported box of chocolates: 11.85"),
                call("Total: 6.70"),
                call("Total: 74.68"),
            ]
        self.assertSequenceEqual(expected_calls, patch_print.call_args_list)
