from decimal import Decimal
from pathlib import Path
import re
from typing import List, Tuple, Union


class InputParser:
    @classmethod
    def parse_item_attributes_from_file(
        cls, path_to_input_file: Union[Path, str]
    ) -> List[Tuple[str, int, Decimal, bool]]:
        items_attributes = []

        with open(path_to_input_file, "r") as f:
            for line in f.readlines():
                (
                    quantity,
                    description,
                    shelf_price,
                ) = cls.parse_item_info_from_input_line(line)
                name, is_imported = cls.parse_name_and_origin_from_description(
                    description
                )
                items_attributes.append((name, quantity, shelf_price, is_imported))

        return items_attributes

    @staticmethod
    def parse_item_info_from_input_line(input_line: str) -> Tuple[int, str, Decimal]:
        quantity_and_description, shelf_price_text = input_line.split(" at ")

        shelf_price = Decimal(shelf_price_text)

        PATTERN_TEXT = r"(?P<quantity>\d+) (?P<description>[\w\s]+)"
        pattern = re.compile(PATTERN_TEXT)
        match = pattern.match(quantity_and_description)
        quantity = int(match.group("quantity"))
        description = match.group("description")

        return quantity, description, shelf_price

    @staticmethod
    def parse_name_and_origin_from_description(description) -> Tuple[str, bool]:
        if "imported" in description:
            name = " ".join(description.replace("imported", "").split())
            return name, True
        else:
            return description, False
