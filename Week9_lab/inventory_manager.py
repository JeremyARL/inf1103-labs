import json
from pathlib import Path

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


FILE_PATH = Path(__file__).parent / "inventory.json"


def load_inventory():
    inventory = Inventory()

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Inventory data must be a list.")

        for item in data:
            try:
                product_type = item.get("type")

                if product_type == "physical":
                    product = PhysicalProduct(
                        item["id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["weight"]
                    )

                elif product_type == "digital":
                    product = DigitalProduct(
                        item["id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["download_size"]
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


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        data.append(product.to_dict())

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


def main():
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

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("Add New Product")
            print("1. Physical Product")
            print("2. Digital Product")

            product_type = input("Select product type: ")

            if product_type not in ("1", "2"):
                print("Invalid product type.")
                continue

            product_id = input("Product ID: ")
            name = input("Product Name: ")

            if inventory.search_product(product_id) is not None:
                print("Product ID already exists.")
                continue

            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))

                if price < 0 or stock < 0:
                    print("Price and stock cannot be negative.")
                    continue

                if product_type == "1":
                    weight = float(input("Weight (kg): "))

                    if weight < 0:
                        print("Weight cannot be negative.")
                        continue

                    product = PhysicalProduct(
                        product_id, name, price, stock, weight
                    )

                else:
                    download_size = float(input("Download Size (MB): "))

                    if download_size < 0:
                        print("Download size cannot be negative.")
                        continue

                    product = DigitalProduct(
                        product_id, name, price, stock, download_size
                    )

            except ValueError:
                print("Invalid numeric input.")
                continue

            inventory.add_product(product)
            print("Product added successfully!")

        elif option == "3":
            print("Update Stock")

            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)

            if product is not None:
                print("Product Found:")
                product.display_information()

                try:
                    new_stock = int(input("New Stock Quantity: "))

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

        elif option == "4":
            print("Search Product")

            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)

            if product is not None:
                print("Product Found:")
                print("-" * 48)
                product.display_information()
                print("Fulfilment:", product.get_fulfilment_info())
                print("-" * 48)

            else:
                print("Product not found.")

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)

        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please enter 1 to 6.")


if __name__ == "__main__":
    main()
