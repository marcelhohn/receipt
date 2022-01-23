import argparse
import subprocess
import pathlib
from unittest import TestCase
from unittest.mock import call, patch


from receipt.main import create_parser, main, print_receipt


class PrintReceipt(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.here = pathlib.Path(__file__).parent.resolve()

    @patch("builtins.print")
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

    @patch("builtins.print")
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

    @patch("builtins.print")
    def test_print_correct_receipt_input_3(self, patch_print):
        path_to_input_1 = str(self.here / "test_inputs/input_3.txt")

        print_receipt(path_to_input_1)

        expected_calls = [
            call("1 imported bottle of perfume: 32.19"),
            call("1 bottle of perfume: 20.89"),
            call("1 packet of headache pills: 9.75"),
            call("1 imported box of chocolates: 11.85"),
            call("Sales Taxes: 6.70"),
            call("Total: 74.68"),
        ]
        self.assertSequenceEqual(expected_calls, patch_print.call_args_list)


class CLI(TestCase):
    def test_cli_command(self):
        # We need to run this as a subprocess to supress the output of the help message
        completed_process = subprocess.run("receipt -h", stdout=subprocess.PIPE)

        self.assertEqual(0, completed_process.returncode)


class ParserCreation(TestCase):
    def setUp(self) -> None:
        self.parser = create_parser()

    def test_parser_has_correct_input_field(self):
        args = self.parser.parse_args(["test_input.txt"])
        self.assertEqual(args.input, "test_input.txt")


class Main(TestCase):
    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(input="test_input.txt"),
    )
    @patch("receipt.main.print_receipt")
    def test_main_calls_print_receipt_with_input_argument(
        self, patch_print_receipt, patch_parse_args
    ):
        main()

        patch_print_receipt.assert_called_once_with("test_input.txt")
