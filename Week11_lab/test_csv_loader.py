from csv_loader import load_products_from_csv
from supplier import Supplier


class FakeInventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)


def test_valid_and_invalid_csv_rows(tmp_path):
    csv_file = tmp_path / "products.csv"

    csv_file.write_text(
        "product_type,product_id,name,price,stock_quantity,weight,download_size\n"
        "physical,P001,Desk Lamp,25.00,10,1.5,\n"
        "digital,D001,Photo Editor,49.90,100,,250\n"
        "service,S001,Installation,30.00,5,,\n"
        "physical,P002,Office Chair,abc,3,8.0,\n"
        "physical,P003,Monitor Stand,39.50,7,2.5,\n"
    )

    inventory = FakeInventory()
    supplier = Supplier("SUP001", "Demo Supplier", "demo@example.com")

    count = load_products_from_csv(csv_file, inventory, supplier)

    assert count == 3
    assert len(inventory.products) == 3


def test_missing_csv_file(tmp_path, capsys):
    inventory = FakeInventory()
    supplier = Supplier("SUP001", "Demo Supplier", "demo@example.com")

    count = load_products_from_csv(
        tmp_path / "missing.csv", inventory, supplier
    )

    output = capsys.readouterr().out

    assert count == 0
    assert "CSV file not found." in output
    assert "Load attempt finished." in output


def test_invalid_price_is_skipped(tmp_path):
    csv_file = tmp_path / "products.csv"

    csv_file.write_text(
        "product_type,product_id,name,price,stock_quantity,weight,download_size\n"
        "physical,P001,Desk Lamp,-25.00,10,1.5,\n"
    )

    inventory = FakeInventory()
    supplier = Supplier("SUP001", "Demo Supplier", "demo@example.com")

    count = load_products_from_csv(csv_file, inventory, supplier)

    assert count == 0
    assert len(inventory.products) == 0
