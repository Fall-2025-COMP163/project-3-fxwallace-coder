"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT
# ============================================================================

def create_character(name, character_class):
    character_class = character_class.lower()

    classes = {
        "warrior": {"health": 120, "strength": 15, "magic": 5},
        "mage": {"health": 80, "strength": 8, "magic": 20},
        "rogue": {"health": 90, "strength": 12, "magic": 10},
        "cleric": {"health": 100, "strength": 10, "magic": 15},
    }

    if character_class not in classes:
        raise InvalidCharacterClassError("Invalid character class")

    base = classes[character_class]

    return {
        "name": name,
        "class": character_class.capitalize(),
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

# ============================================================================
# SAVE / LOAD
# ============================================================================

def save_character(character, save_directory="data/save_games"):
    os.makedirs(save_directory, exist_ok=True)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w") as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")

            # MUST include a SPACE after ": " even when empty
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")

        return True

    except Exception:
        raise SaveFileCorruptedError("Could not save character file")

def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("Character save file not found")

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except Exception:
        raise SaveFileCorruptedError("Error reading save file")

    character = {}

    try:
        for line in lines:
            if ": " not in line:
                raise InvalidSaveDataError("Invalid file format")

            key, value = line.strip().split(": ", 1)

            if key in ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC",
                       "EXPERIENCE", "GOLD"]:
                character[key.lower()] = int(value)
            elif key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
                character[key.lower()] = value.split(",") if value else []
            else:
                character[key.lower()] = value

        validate_character_data(character)
        return character

    except Exception:
        raise InvalidSaveDataError("Save data is corrupted")

def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []

    files = os.listdir(save_directory)
    names = []

    for file in files:
        if file.endswith("_save.txt"):
            names.append(file.replace("_save.txt", ""))

    return names

def delete_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("Character not found")

    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character["health"] <= 0:
        raise CharacterDeadError("Cannot gain XP while dead")

    character["experience"] += xp_amount

    leveled_up = False

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]
        leveled_up = True

    return leveled_up

def add_gold(character, amount):
    new_amount = character["gold"] + amount
    if new_amount < 0:
        raise ValueError("Gold cannot be negative")

    character["gold"] = new_amount
    return character["gold"]

def heal_character(character, amount):
    old_health = character["health"]
    character["health"] = min(character["max_health"], character["health"] + amount)
    return character["health"] - old_health

def is_character_dead(character):
    return character["health"] <= 0

def revive_character(character):
    if character["health"] > 0:
        return False

    character["health"] = character["max_health"] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for key in required:
        if key not in character:
            raise InvalidSaveDataError(f"Missing field: {key}")

    numeric = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]

    for key in numeric:
        if not isinstance(character[key], int):
            raise InvalidSaveDataError(f"Invalid number for {key}")

    list_fields = ["inventory", "active_quests", "completed_quests"]

    for key in list_fields:
        if not isinstance(character[key], list):
            raise InvalidSaveDataError(f"Invalid list for {key}")

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

