import unittest
from inspect import isabstract

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from supplier import Supplier


class TestProducts(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier(
            "S001",
            "ABC Electronics",
            "contact@abcelectronics.com"
        )

        self.physical = PhysicalProduct(
            "P001", "Laptop", 1200.0, 20, 2.5, self.supplier
        )

        self.digital = DigitalProduct(
            "D001", "Software", 99.0, 100, 500.0, self.supplier
        )

    def test_physical_product_inheritance(self):
        self.assertIsInstance(self.physical, Product)

    def test_digital_product_inheritance(self):
        self.assertIsInstance(self.digital, Product)

    def test_product_is_abstract(self):
        self.assertTrue(isabstract(Product))

        with self.assertRaises(TypeError):
            Product(
                "P003", "Generic", 10.0, 5, self.supplier
            )

    def test_physical_product_weight(self):
        data = self.physical.to_dict()

        self.assertEqual(data["type"], "physical")
        self.assertEqual(data["weight"], 2.5)

    def test_digital_product_download_size(self):
        data = self.digital.to_dict()

        self.assertEqual(data["type"], "digital")
        self.assertEqual(data["download_size"], 500.0)

    def test_physical_product_shipping(self):
        self.assertIsInstance(self.physical, CanBeShipped)

        self.assertEqual(
            self.physical.calculate_shipping_cost(), 12.5
        )

    def test_digital_product_no_shipping(self):
        self.assertNotIsInstance(self.digital, CanBeShipped)

        self.assertFalse(
            hasattr(self.digital, "calculate_shipping_cost")
        )

    def test_fulfilment_information(self):
        self.assertEqual(
            self.physical.get_fulfilment_info(),
            "This product requires physical shipping."
        )

        self.assertEqual(
            self.digital.get_fulfilment_info(),
            "This product is delivered digitally."
        )

    def test_stock_update(self):
        self.physical.update_stock(50)

        self.assertEqual(
            self.physical.to_dict()["stock"], 50
        )


if __name__ == "__main__":
    unittest.main()
