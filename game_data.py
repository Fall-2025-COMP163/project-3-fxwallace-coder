"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module
game_data.py
Name: [Your Name Here]

AI Usage: Used ChatGPT for help writing simple parsing functions.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

from custom_exceptions import ItemNotFoundError, InventoryFullError

MAX_INVENTORY_SIZE = 20

def add_item_to_inventory(character, item_id):
    # inventory full
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    character["inventory"].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not found")

    character["inventory"].remove(item_id)
    return True

def has_item(character, item_id):
    return item_id in character["inventory"]

def count_item(character, item_id):
    return character["inventory"].count(item_id)

def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character["inventory"])

def clear_inventory(character):
    removed = character["inventory"][:]
    character["inventory"].clear()
    return removed



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

