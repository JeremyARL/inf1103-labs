inventory = 0
failed_entries = 0
deliveries_processed = 0


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


while True:
    stock = get_valid_input()

    if stock == "quit":
        generate_report(deliveries_processed, failed_entries)
        break

    if stock is None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)

    tax = calculate_tax(stock)
    print("Tax:", tax)

    deliveries_processed += 1

    if inventory > 500:
        print("Alert: Inventory exceeds storage capacity!")
        break