import argparse

from receipt.input_parser import InputParser
from receipt.item import Item
from receipt.shopping_basket import ShoppingBasket


def main():
    parser = argparse.ArgumentParser(
        description="An application for generating receipt details of shopping baskets"
    )
    parser.add_argument("input", help="Path to the input file")
    args = parser.parse_args()
    
    print_receipt(args.input)


def print_receipt(input_file: str):
    items_attributes = InputParser.parse_item_attributes_from_file(input_file)
    items = [Item(*item_attributes) for item_attributes in items_attributes]
    shopping_basket = ShoppingBasket(items)
    shopping_basket.print()


if __name__ == "__main__":
    main()
