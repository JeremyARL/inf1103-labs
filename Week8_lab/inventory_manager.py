import json
from pathlib import Path

from product import Product
from inventory import Inventory


FILE_PATH = Path(__file__).parent / "inventory.json"


def load_inventory():
    inventory = Inventory()

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            product = Product(
                item["id"],
                item["name"],
                item["price"],
                item["stock"]
            )
            inventory.add_product(product)

        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")

    except (json.JSONDecodeError, TypeError, KeyError):
        print("Invalid inventory file. Starting with empty inventory.")
        inventory = Inventory()

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

            product_id = input("Product ID: ")
            name = input("Product Name: ")

            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))
            except ValueError:
                print("Invalid price or stock quantity.")
                continue

            product = Product(product_id, name, price, stock)
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