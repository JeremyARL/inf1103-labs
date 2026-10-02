import json
import os

def load_inventory():
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as file:
            inventory = json.load(file)

        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return inventory

    else:
        print("inventory.json not found.")
        return []

inventory = load_inventory()
