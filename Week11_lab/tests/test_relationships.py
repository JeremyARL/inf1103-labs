import unittest
from io import StringIO
from contextlib import redirect_stdout
from typing import get_type_hints

from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine


class TestRelationships(unittest.TestCase):

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

    # 1. ASSOCIATION
    def test_supplier_association(self):
        self.assertIs(
            self.physical.supplier,
            self.digital.supplier
        )

        supplier = Supplier(
            "S002", "Another Supplier", "test@example.com"
        )

        product = PhysicalProduct(
            "P002", "Mouse", 25.0, 10, 0.2, supplier
        )

        del supplier

        self.assertEqual(
            product.supplier.to_dict()["supplier_id"],
            "S002"
        )

    # 2. SUPPLIER SERIALIZATION
    def test_supplier_serialization(self):
        data = self.physical.to_dict()

        self.assertEqual(
            data["supplier"]["supplier_id"],
            "S001"
        )

        self.assertEqual(
            data["supplier"]["name"],
            "ABC Electronics"
        )

    # 3. AGGREGATION
    def test_inventory_aggregation_transfer(self):
        inventory_a = Inventory()
        inventory_b = Inventory()

        inventory_a.add_product(self.physical)

        removed = inventory_a.remove_product("P001")

        self.assertIs(removed, self.physical)
        self.assertIsNone(inventory_a.find_product("P001"))

        inventory_b.add_product(self.physical)

        self.assertIs(
            inventory_b.find_product("P001"),
            self.physical
        )

    # 4. PRODUCT NOT FOUND
    def test_inventory_missing_product(self):
        inventory = Inventory()

        self.assertIsNone(
            inventory.find_product("UNKNOWN")
        )

        self.assertIsNone(
            inventory.remove_product("UNKNOWN")
        )

    # 5. COMPOSITION
    def test_order_composition(self):
        order_a = Order("O001")
        order_b = Order("O002")

        order_a.add_order_line(self.physical, 2)
        order_b.add_order_line(self.physical, 1)

        line_a = order_a.get_order_lines()[0]
        line_b = order_b.get_order_lines()[0]

        self.assertIsNot(line_a, line_b)
        self.assertIs(line_a.product, self.physical)
        self.assertIs(line_b.product, self.physical)

        self.assertEqual(len(order_a.get_order_lines()), 1)
        self.assertEqual(len(order_b.get_order_lines()), 1)

    # 6. ORDER TOTALS AND REMOVAL
    def test_order_totals_and_removal(self):
        order_a = Order("O001")
        order_b = Order("O002")

        order_a.add_order_line(self.physical, 2)
        order_a.add_order_line(self.digital, 1)
        order_b.add_order_line(self.physical, 1)

        self.assertEqual(order_a.calculate_total(), 2499.0)
        self.assertEqual(order_b.calculate_total(), 1200.0)

        self.assertTrue(order_a.remove_order_line("P001"))

        self.assertEqual(order_a.calculate_total(), 99.0)
        self.assertEqual(order_b.calculate_total(), 1200.0)

        self.assertEqual(
            self.physical.get_product_id(),
            "P001"
        )

        with self.assertRaises(ValueError):
            order_a.add_order_line(self.physical, 0)

    # 7. LISKOV SUBSTITUTION PRINCIPLE
    def test_lsp(self):
        def show_product_details(product: Product) -> str:
            output = StringIO()

            with redirect_stdout(output):
                product.display_information()
                print(product.get_fulfilment_info())

            return output.getvalue()

        physical_output = show_product_details(self.physical)
        digital_output = show_product_details(self.digital)

        self.assertIn("Laptop", physical_output)
        self.assertIn("Software", digital_output)

        self.physical.update_stock(30)
        self.digital.update_stock(50)

        self.assertEqual(
            self.physical.to_dict()["stock"], 30
        )

        self.assertEqual(
            self.digital.to_dict()["stock"], 50
        )

    # 8. POLYMORPHISM
    def test_polymorphism(self):
        inventory = Inventory()

        inventory.add_product(self.physical)
        inventory.add_product(self.digital)

        messages = []

        for product in inventory.get_products():
            product.display_information()
            messages.append(product.get_fulfilment_info())

        self.assertEqual(
            messages,
            [
                "This product requires physical shipping.",
                "This product is delivered digitally."
            ]
        )

    # 9. TYPE HINTS
    def test_relationship_type_hints(self):
        self.assertIs(
            get_type_hints(Inventory.add_product)["product"],
            Product
        )

        self.assertEqual(
            get_type_hints(Inventory.find_product)["return"],
            Product | None
        )

        self.assertIs(
            get_type_hints(Order.add_order_line)["product"],
            Product
        )

        self.assertEqual(
            get_type_hints(Order.get_order_lines)["return"],
            list[OrderLine]
        )

        self.assertIs(
            get_type_hints(OrderLine.calculate_subtotal)["return"],
            float
        )


if __name__ == "__main__":
    unittest.main()
