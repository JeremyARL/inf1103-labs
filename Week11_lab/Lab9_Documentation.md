# INF1103 Lab 9 – Design Patterns and Error Handling

## 1. Strategy Pattern

Implemented the Strategy Pattern using an abstract
DiscountStrategy class and four concrete strategies:

- NoDiscount
- PercentageDiscount
- BulkDiscount
- StudentDiscount

The Order class uses a discount strategy to calculate
discounts without requiring separate conditional logic
for each discount type.

This makes it easier to introduce additional discount
strategies without modifying the Order class.

## 2. Factory Pattern

Implemented ProductFactory to create different product
types.

- PhysicalProduct requires weight information.
- DigitalProduct requires download size information.
- Unsupported product types raise a ValueError.

The factory centralises product creation and reduces
the need to construct different product classes
throughout the application.

## 3. Input Validation

Added validation to prevent invalid product prices,
negative stock quantities and invalid order quantities.

Created input_helpers.py to handle invalid numeric
input using try-except and repeated prompts.

## 4. Exception Handling and CSV Loading

Created csv_loader.py to import products from a CSV file.

The loader:
- Reads product data using csv.DictReader.
- Uses ProductFactory to create product objects.
- Skips invalid product records.
- Handles missing CSV files.
- Uses try, except, else and finally.
- Continues processing when individual rows are invalid.

The sample products.csv contains five records,
of which three are valid.

## 5. Automated Testing

Used pytest to test existing functionality and
the new CSV loading features.

CSV tests cover:
- Valid and invalid product records.
- Missing CSV files.
- Invalid product prices.

Final test result:

27 passed in 0.02s

Command used:

python3 -m pytest -q

## 6. UML Class Diagram

Created Lab9_UML.drawio using draw.io to illustrate:

- Product inheritance relationships.
- The CanBeShipped interface.
- DiscountStrategy and its subclasses.
- ProductFactory dependencies.
- Relationships among Order, OrderLine, Inventory,
  Product and Supplier.

The diagram documents the application's OOP structure
and the design patterns implemented in Lab 9.
