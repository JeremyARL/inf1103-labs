inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or quit): ")

    if stock == "quit":
        break

    if not stock.isdigit():
        print("Invalid input. Please enter a number.")
        failed_entries += 1
        continue

    stock = int(stock)

    if stock < 0:
        print("Negative number are not allowed")
        failed_entries += 1
        continue

    inventory += stock
    print("Current Inventory:",inventory)

    if inventory > 500:
        print("Alert: Inventory exceeds storage capacity!")
        break


print("Total Units Processed:", inventory)
print("Number of Failure/Rejected Entries:", failed_entries)