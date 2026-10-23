from product import Product

laptop = Product("P001", "Laptop", 1200.00, 15)

laptop.display_information()

laptop.update_stock(50)

print("After updating stock:")
laptop.display_information()