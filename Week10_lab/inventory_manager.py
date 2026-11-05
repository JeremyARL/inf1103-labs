import json
from pathlib import Path

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from supplier import Supplier


FILE_PATH = Path(__file__).parent / "inventory.json"


# ==========================================
# LOAD INVENTORY
# ==========================================

def load_inventory() -> Inventory:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Inventory data must be a list.")

        for item in data:
            try:
                product_type = item.get("type")

                # Get supplier information
                supplier_data = item.get("supplier")

                # Support old Week 9 products without suppliers
                if supplier_data is None:
                    supplier_data = {
                        "supplier_id": "S000",
                        "name": "Unassigned Supplier",
                        "contact_email": "Not provided"
                    }

                supplier_id = supplier_data["supplier_id"]

                # Reuse existing Supplier objects
                if supplier_id not in suppliers:
                    suppliers[supplier_id] = Supplier(
                        supplier_id,
                        supplier_data["name"],
                        supplier_data["contact_email"]
                    )

                supplier = suppliers[supplier_id]

                # Create PhysicalProduct
                if product_type == "physical":
                    product = PhysicalProduct(
                        item["id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["weight"],
                        supplier
                    )

                # Create DigitalProduct
                elif product_type == "digital":
                    product = DigitalProduct(
                        item["id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["download_size"],
                        supplier
                    )

                else:
                    print("Unknown product type. Skipping product.")
                    continue

                inventory.add_product(product)

            except (KeyError, TypeError, ValueError, AttributeError):
                print("Invalid product data. Skipping product.")

        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")

    except (json.JSONDecodeError, TypeError, ValueError):
        print("Invalid inventory file. Starting with empty inventory.")

    return inventory


# ==========================================
# SAVE INVENTORY
# ==========================================

def save_inventory(inventory: Inventory) -> None:
    data = []

    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


# ==========================================
# MAIN INVENTORY MANAGEMENT SYSTEM
# ==========================================

def main() -> None:
    inventory = load_inventory()

    while True:
        print("========================================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("========================================")
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        option = input("Enter option: ")

        # ==================================
        # OPTION 1: DISPLAY ALL PRODUCTS
        # ==================================

        if option == "1":
            inventory.display_all()

        # ==================================
        # OPTION 2: ADD PRODUCT
        # ==================================

        elif option == "2":
            print("Add New Product")
            print("1. Physical Product")
            print("2. Digital Product")

            product_type = input("Select product type: ")

            if product_type not in ("1", "2"):
                print("Invalid product type.")
                continue

            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()

            if not product_id or not name:
                print("Product ID and name cannot be empty.")
                continue

            if inventory.search_product(product_id) is not None:
                print("Product ID already exists.")
                continue

            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))

                if price < 0 or stock < 0:
                    print("Price and stock cannot be negative.")
                    continue

                # --------------------------
                # SUPPLIER ASSOCIATION
                # --------------------------

                supplier_id = input("Supplier ID: ").strip()

                if not supplier_id:
                    print("Supplier ID cannot be empty.")
                    continue

                supplier = None

                # Search for an existing Supplier
                for existing_product in inventory.get_products():
                    existing_supplier = existing_product.supplier

                    if (
                        existing_supplier.to_dict()["supplier_id"]
                        == supplier_id
                    ):
                        supplier = existing_supplier
                        break

                # Create Supplier if not found
                if supplier is None:
                    supplier_name = input(
                        "Supplier Name: "
                    ).strip()

                    supplier_email = input(
                        "Supplier Contact Email: "
                    ).strip()

                    if not supplier_name or not supplier_email:
                        print(
                            "Supplier name and email cannot be empty."
                        )
                        continue

                    supplier = Supplier(
                        supplier_id,
                        supplier_name,
                        supplier_email
                    )

                else:
                    print("Using existing supplier.")

                # --------------------------
                # PHYSICAL PRODUCT
                # --------------------------

                if product_type == "1":
                    weight = float(input("Weight (kg): "))

                    if weight < 0:
                        print("Weight cannot be negative.")
                        continue

                    product = PhysicalProduct(
                        product_id,
                        name,
                        price,
                        stock,
                        weight,
                        supplier
                    )

                # --------------------------
                # DIGITAL PRODUCT
                # --------------------------

                else:
                    download_size = float(
                        input("Download Size (MB): ")
                    )

                    if download_size < 0:
                        print("Download size cannot be negative.")
                        continue

                    product = DigitalProduct(
                        product_id,
                        name,
                        price,
                        stock,
                        download_size,
                        supplier
                    )

            except ValueError:
                print("Invalid numeric input.")
                continue

            inventory.add_product(product)
            print("Product added successfully!")

        # ==================================
        # OPTION 3: UPDATE STOCK
        # ==================================

        elif option == "3":
            print("Update Stock")

            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)

            if product is not None:
                print("Product Found:")
                product.display_information()

                try:
                    new_stock = int(
                        input("New Stock Quantity: ")
                    )

                    if new_stock < 0:
                        print("Stock cannot be negative.")
                        continue

                except ValueError:
                    print("Invalid stock quantity.")
                    continue

                product.update_stock(new_stock)
                print("Stock updated successfully!")

            else:
                print("Product not found.")

        # ==================================
        # OPTION 4: SEARCH PRODUCT
        # ==================================

        elif option == "4":
            print("Search Product")

            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)

            if product is not None:
                print("Product Found:")
                print("-" * 48)
                product.display_information()
                print(
                    "Fulfilment:",
                    product.get_fulfilment_info()
                )
                print("-" * 48)

            else:
                print("Product not found.")

        # ==================================
        # OPTION 5: SAVE INVENTORY
        # ==================================

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        # ==================================
        # OPTION 6: EXIT
        # ==================================

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print(
                "Thank you for using Inventory Management System."
            )
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please enter 1 to 6.")


if __name__ == "__main__":
    main()
