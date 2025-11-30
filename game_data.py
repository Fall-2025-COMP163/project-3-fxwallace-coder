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

# =====================================================================
# LOAD QUESTS
# =====================================================================

def load_quests(filename="data/quests.txt"):
    if not os.path.exists(filename):
        raise MissingDataFileError("Quest file not found.")

    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
    except:
        raise CorruptedDataError("Could not read quest file.")

    quests = {}
    block = []

    for line in lines + [""]:
        if line.strip() == "":
            if len(block) > 0:
                quest = parse_quest_block(block)
                validate_quest_data(quest)
                quests[quest["quest_id"]] = quest
                block = []
        else:
            block.append(line)

    return quests

# =====================================================================
# LOAD ITEMS
# =====================================================================

def load_items(filename="data/items.txt"):
    if not os.path.exists(filename):
        raise MissingDataFileError("Item file not found.")

    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
    except:
        raise CorruptedDataError("Could not read item file.")

    items = {}
    block = []

    for line in lines + [""]:
        if line.strip() == "":
            if len(block) > 0:
                item = parse_item_block(block)
                validate_item_data(item)
                items[item["item_id"]] = item
                block = []
        else:
            block.append(line)

    return items

# =====================================================================
# VALIDATION
# =====================================================================

def validate_quest_data(q):
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold",
        "required_level", "prerequisite"
    ]

    for r in required:
        if r not in q:
            raise InvalidDataFormatError("Missing quest field: " + r)

    return True


def validate_item_data(i):
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for r in required:
        if r not in i:
            raise InvalidDataFormatError("Missing item field: " + r)

    if i["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError("Invalid item type.")

    return True

# =====================================================================
# PARSE QUEST
# =====================================================================

def parse_quest_block(lines):
    quest = {}

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Bad quest line format.")
        key, value = line.split(": ", 1)

        if key == "QUEST_ID":
            quest["quest_id"] = value
        elif key == "TITLE":
            quest["title"] = value
        elif key == "DESCRIPTION":
            quest["description"] = value
        elif key == "REWARD_XP":
            quest["reward_xp"] = int(value)
        elif key == "REWARD_GOLD":
            quest["reward_gold"] = int(value)
        elif key == "REQUIRED_LEVEL":
            quest["required_level"] = int(value)
        elif key == "PREREQUISITE":
            quest["prerequisite"] = value

    return quest

# =====================================================================
# PARSE ITEM
# =====================================================================

def parse_item_block(lines):
    item = {}

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Bad item line format.")
        key, value = line.split(": ", 1)

        if key == "ITEM_ID":
            item["item_id"] = value
        elif key == "NAME":
            item["name"] = value
        elif key == "TYPE":
            item["type"] = value
        elif key == "EFFECT":
            # example: "strength:5"
            stat, num = value.split(":")
            item["effect"] = {stat: int(num)}
        elif key == "COST":
            item["cost"] = int(value)
        elif key == "DESCRIPTION":
            item["description"] = value

    return item

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

