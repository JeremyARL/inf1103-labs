from product_factory import ProductFactory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier

supplier = Supplier("S001", "Test Supplier", "test@example.com")

physical = ProductFactory.create(
    "physical", "P001", "Chair", 100.0, 10, supplier, weight=5.0
)

digital = ProductFactory.create(
    "digital", "D001", "Software", 50.0, 20, supplier, download_size=100.0
)

print(isinstance(physical, PhysicalProduct))
print(isinstance(digital, DigitalProduct))

try:
    ProductFactory.create(
        "service", "S002", "Installation", 30.0, 5, supplier
    )
except ValueError as error:
    print(error)