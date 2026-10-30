import unittest
import tempfile

from pathlib import Path
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory_manager import save_inventory, load_inventory


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()

        self.physical = PhysicalProduct(
            "P001", "Laptop", 1200.0, 20, 2.5
        )

        self.digital = DigitalProduct(
            "D001", "Software", 99.0, 100, 500.0
        )

        self.inventory.add_product(self.physical)
        self.inventory.add_product(self.digital)

    def test_add_and_search_products(self):
        self.assertEqual(
            self.inventory.search_product("P001"),
            self.physical
        )

        self.assertEqual(
            self.inventory.search_product("D001"),
            self.digital
        )

        self.assertIsNone(
            self.inventory.search_product("UNKNOWN")
        )

    def test_inventory_contains_both_product_types(self):
        products = self.inventory.get_products()

        self.assertEqual(len(products), 2)
        self.assertIsInstance(products[0], PhysicalProduct)
        self.assertIsInstance(products[1], DigitalProduct)

    def test_display_all_products(self):
        output = StringIO()

        with redirect_stdout(output):
            self.inventory.display_all()

        result = output.getvalue()

        self.assertIn("Weight: 2.5 kg", result)
        self.assertIn("Download Size: 500.0 MB", result)

    def test_save_and_load_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            test_file = Path(directory) / "inventory.json"

            with patch("inventory_manager.FILE_PATH", test_file):
                with redirect_stdout(StringIO()):
                    save_inventory(self.inventory)
                    loaded_inventory = load_inventory()

            physical = loaded_inventory.search_product("P001")
            digital = loaded_inventory.search_product("D001")

            self.assertIsInstance(physical, PhysicalProduct)
            self.assertIsInstance(digital, DigitalProduct)

            self.assertEqual(
                physical.to_dict()["weight"], 2.5
            )

            self.assertEqual(
                digital.to_dict()["download_size"], 500.0
            )

    def test_missing_json_file(self):
        with tempfile.TemporaryDirectory() as directory:
            test_file = Path(directory) / "missing.json"

            with patch("inventory_manager.FILE_PATH", test_file):
                with redirect_stdout(StringIO()):
                    loaded_inventory = load_inventory()

            self.assertEqual(
                len(loaded_inventory.get_products()), 0
            )

    def test_invalid_json_file(self):
        with tempfile.TemporaryDirectory() as directory:
            test_file = Path(directory) / "inventory.json"
            test_file.write_text(
                "invalid json",
                encoding="utf-8"
            )

            with patch("inventory_manager.FILE_PATH", test_file):
                with redirect_stdout(StringIO()):
                    loaded_inventory = load_inventory()

            self.assertEqual(
                len(loaded_inventory.get_products()), 0
            )


if __name__ == "__main__":
    unittest.main()
