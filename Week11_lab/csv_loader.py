import csv
from product_factory import ProductFactory


def load_products_from_csv(file_path, inventory, supplier):
    count = 0

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):
                try:
                    weight = (
                        float(row["weight"])
                        if row["weight"] else None
                    )

                    download_size = (
                        float(row["download_size"])
                        if row["download_size"] else None
                    )

                    product = ProductFactory.create(
                        product_type=row["product_type"],
                        product_id=row["product_id"],
                        name=row["name"],
                        price=float(row["price"]),
                        stock=int(row["stock_quantity"]),
                        supplier=supplier,
                        weight=weight,
                        download_size=download_size
                    )

                    inventory.add_product(product)

                except (ValueError, KeyError, TypeError) as error:
                    print(f"Skipping row {row_number}: {error}")

                else:
                    count += 1

    except FileNotFoundError:
        print("CSV file not found.")

    except OSError as error:
        print(f"Error reading CSV file: {error}")

    else:
        print(f"{count} products loaded.")

    finally:
        print("Load attempt finished.")

    return count
