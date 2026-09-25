def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            inventory = int(lines[0].strip())

            transaction_history = []

            for line in lines[1:]:
                transaction_history.append(int(line.strip()))

            return inventory, transaction_history

    except FileNotFoundError:
        return 0, []


def save_inventory(inventory, transaction_history):
    with open("inventory.txt", "w") as file:
        file.write(str(inventory) + "\n")

        for transaction in transaction_history:
            file.write(str(transaction) + "\n")


def get_valid_input():
    while True:
        stock = input("Enter stock quantity (or quit): ")

        if stock == "quit":
            return "quit"

        if not stock.isdigit():
            print("Invalid input. Please enter a number.")
            return None

        stock = int(stock)

        if stock < 0:
            print("Negative numbers are not allowed")
            return None

        return stock


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory, transaction_history = load_inventory()

failed_entries = 0
deliveries_processed = 0


while True:
    stock = get_valid_input()

    if stock == "quit":
        save_inventory(inventory, transaction_history)
        generate_report(deliveries_processed, failed_entries)
        break

    if stock is None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)

    transaction_history.append(stock)

    tax = calculate_tax(stock)
    print("Tax:", tax)

    deliveries_processed += 1

    if inventory > 500:
        print("Alert: Inventory exceeds storage capacity!")
        save_inventory(inventory, transaction_history)
        break