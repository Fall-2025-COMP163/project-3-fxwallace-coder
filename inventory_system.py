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
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError("Item not found")

    # item_data is the data for the specific item
    item = item_data

    # only consumables can be used
    if item.get("type") != "consumable":
        raise InvalidItemTypeError("Item is not consumable")

    # parse effect like "health:20" or "strength:3"
    eff = item.get("effect", "")
    if ":" in eff:
        stat, val = eff.split(":", 1)
        val = int(val)
        if stat == "health":
            character["health"] = min(character.get("max_health", 0), character.get("health", 0) + val)
        elif stat == "max_health":
            character["max_health"] = character.get("max_health", 0) + val
        elif stat == "strength":
            character["strength"] = character.get("strength", 0) + val
        elif stat == "magic":
            character["magic"] = character.get("magic", 0) + val

    # remove consumable from inventory
    character["inventory"].remove(item_id)
    return True



def equip_weapon(character, item_id, item_data):
    inv = character.setdefault("inventory", [])
    if item_id not in inv:
        raise ItemNotFoundError("Weapon not in inventory")

    item = item_data  # item_data is the item's info
    if item.get("type") != "weapon":
        raise InvalidItemTypeError("Item is not a weapon")

    # Unequip old weapon if present
    old = character.get("equipped_weapon")
    if old:
        inv.append(old)
        # NOTE: if you gave stat bonus for old, you'd remove it here

    # Apply weapon effect e.g., "strength:5"
    eff = item.get("effect", "")
    if ":" in eff:
        stat, val = eff.split(":", 1)
        val = int(val)
        if stat == "strength":
            character["strength"] = character.get("strength", 0) + val
        elif stat == "magic":
            character["magic"] = character.get("magic", 0) + val

    character["equipped_weapon"] = item_id
    inv.remove(item_id)
    return True


def equip_armor(character, item_id, item_data):
    inv = character.setdefault("inventory", [])
    if item_id not in inv:
        raise ItemNotFoundError("Armor not in inventory")

    item = item_data
    if item.get("type") != "armor":
        raise InvalidItemTypeError("Item is not armor")

    old = character.get("equipped_armor")
    if old:
        inv.append(old)
        # remove old bonuses here if your system tracked them

    eff = item.get("effect", "")
    if ":" in eff:
        stat, val = eff.split(":", 1)
        val = int(val)
        if stat == "max_health":
            character["max_health"] = character.get("max_health", 0) + val
            # ensure current health not above new max (or you can leave it)
            character["health"] = min(character.get("health", 0), character["max_health"])
        elif stat == "magic":
            character["magic"] = character.get("magic", 0) + val

    character["equipped_armor"] = item_id
    inv.remove(item_id)
    return True


# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    # item_data here is the item's info dict (not a dict-of-items)
    item = item_data
    cost = int(item.get("cost", 0))

    if character.get("gold", 0) < cost:
        raise InsufficientResourcesError("Not enough gold")

    if len(character.get("inventory", [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")

    character["gold"] = character.get("gold", 0) - cost
    character.setdefault("inventory", []).append(item_id)
    return True


def sell_item(character, item_id, item_data):
    inv = character.setdefault("inventory", [])
    if item_id not in inv:
        raise ItemNotFoundError("Item not in inventory")

    item = item_data
    price = int(item.get("cost", 0)) // 2

    inv.remove(item_id)
    character["gold"] = character.get("gold", 0) + price
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

