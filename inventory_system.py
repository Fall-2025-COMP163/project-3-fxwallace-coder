"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

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
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not found")

    item = item_data  # Use directly

    if item.get("type") != "consumable":
        raise InvalidItemTypeError("This item cannot be used")

    effect = item.get("effect", "")

    if effect.startswith("heal:"):
        amount = int(effect.split(":")[1])
        character["health"] = min(character["health"] + amount,
                                  character["max_health"])
    
    character["inventory"].remove(item_id)
    return True


def equip_weapon(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Weapon not in inventory")
    
    item = item_data[item_id]
    if item["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon")
    
    # Unequip old weapon if any
    if "equipped_weapon" in character:
        old_weapon = character["equipped_weapon"]
        character["inventory"].append(old_weapon)
    
    # Equip new weapon
    stat, value = item["effect"].split(":")
    value = int(value)
    character[stat] += value
    character["equipped_weapon"] = item_id
    character["inventory"].remove(item_id)
    return True

def equip_armor(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Armor not in inventory")
    
    item = item_data[item_id]
    if item["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor")
    
    # Unequip old armor if any
    if "equipped_armor" in character:
        old_armor = character["equipped_armor"]
        character["inventory"].append(old_armor)
    
    stat, value = item["effect"].split(":")
    value = int(value)
    character[stat] += value
    character["equipped_armor"] = item_id
    character["inventory"].remove(item_id)
    return True

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    # item_data is already the item’s info
    item = item_data  

    cost = item.get("cost", 0)
    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold to purchase item.")
    
    character["gold"] -= cost
    character["inventory"].append(item_id)
    return True


def sell_item(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory")
    
    price = item_data[item_id]["cost"] // 2
    character["inventory"].remove(item_id)
    character["gold"] += price
    return price


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

