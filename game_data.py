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

