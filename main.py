"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
# main.py
# Full simple CLI for Quest Chronicles (freshman-level)
# Uses only these imports (no extras as requested)
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *   # project used this pattern elsewhere

# ---------------------------
# Global game state
# ---------------------------
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ---------------------------
# Helpers for safe calls
# ---------------------------

def safe_load_data():
    """
    Try to load quests and items. If files missing or invalid,
    return False so caller can decide what to do.
    """
    global all_quests, all_items
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
        return True
    except (MissingDataFileError, InvalidDataFormatError, CorruptedDataError) as e:
        print("Data load error:", e)
        return False
    except Exception as e:
        # Unexpected error — print and return False
        print("Unexpected data error:", e)
        return False

# ---------------------------
# Main menu and new/load
# ---------------------------

def main_menu():
    """Show top-level menu and return numeric choice."""
    print("\n=== QUEST CHRONICLES ===")
    print("1) New Game")
    print("2) Load Game")
    print("3) Exit")
    while True:
        choice = input("Choose 1-3: ").strip()
        if choice in ("1","2","3"):
            return int(choice)
        print("Please enter 1, 2, or 3.")

def new_game():
    """Create a character and start the in-game loop."""
    global current_character
    print("\n--- New Game ---")
    name = input("Enter character name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    print("Choose class: Warrior, Mage, Rogue, Cleric")
    class_name = input("Class: ").strip()
    try:
        char = character_manager.create_character(name, class_name)
    except InvalidCharacterClassError:
        print("Invalid class. Try again.")
        return

    # save in memory and to disk (character_manager.save_character returns True/False)
    saved = character_manager.save_character(char)
    if saved:
        print(f"Created and saved character '{name}'.")
    current_character = char
    # Enter game loop
    game_loop()

def load_game():
    """List saved characters and let user load one."""
    global current_character
    print("\n--- Load Game ---")
    # Some character_manager versions have list_saved_characters, others do not.
    try:
        saves = character_manager.list_saved_characters()
    except Exception:
        # Fallback: try to read save directory manually if function missing
        try:
            saves = character_manager.list_saved_characters()
        except Exception:
            # If not available, try to find files in 'data/save_games'
            saves = []
            try:
                import os
                folder = os.path.join("data","save_games")
                if os.path.exists(folder):
                    for fn in os.listdir(folder):
                        if fn.endswith("_save.txt"):
                            saves.append(fn.replace("_save.txt",""))
            except Exception:
                saves = []

    if not saves:
        print("No saved characters found.")
        return

    for i, name in enumerate(saves, start=1):
        print(f"{i}) {name}")
    pick = input("Select number to load: ").strip()
    try:
        idx = int(pick) - 1
        if idx < 0 or idx >= len(saves):
            print("Invalid selection.")
            return
        chosen = saves[idx]
        char = character_manager.load_character(chosen)
        current_character = char
        print(f"Loaded '{chosen}'.")
        game_loop()
    except (ValueError, IndexError):
        print("Invalid input.")
    except CharacterNotFoundError:
        print("Save file missing.")
    except SaveFileCorruptedError:
        print("Save file corrupted.")
    except Exception as e:
        print("Could not load character:", e)

# ---------------------------
# In-game loop and menus
# ---------------------------

def game_loop():
    """Main game loop (in-game menu)."""
    global game_running, current_character
    if current_character is None:
        print("No character active.")
        return

    game_running = True
    print(f"\nWelcome, {current_character['name']} (Level {current_character['level']})")

    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Saved. Returning to main menu.")
            game_running = False
        else:
            print("Invalid choice.")

def game_menu():
    """Show in-game menu; return integer choice."""
    print("\n--- GAME MENU ---")
    print("1) View Character Stats")
    print("2) View Inventory")
    print("3) Quest Menu")
    print("4) Explore (find enemies)")
    print("5) Shop")
    print("6) Save and Quit to Main Menu")
    while True:
        c = input("Choose 1-6: ").strip()
        if c in ("1","2","3","4","5","6"):
            return int(c)
        print("Please enter a number 1-6.")

# ---------------------------
# Actions: Stats, Inventory, Quests, Explore, Shop
# ---------------------------

def view_character_stats():
    """Print basic character info and quest progress."""
    global current_character, all_quests
    c = current_character
    print("\n--- CHARACTER STATS ---")
    print(f"Name: {c.get('name')}")
    print(f"Class: {c.get('class')}")
    print(f"Level: {c.get('level')}  XP: {c.get('experience')}")
    print(f"HP: {c.get('health')}/{c.get('max_health')}")
    print(f"Strength: {c.get('strength')}  Magic: {c.get('magic')}")
    print(f"Gold: {c.get('gold')}")
    print(f"Active quests: {len(c.get('active_quests', []))}")
    print(f"Completed quests: {len(c.get('completed_quests', []))}")
    if all_quests:
        try:
            pct = quest_handler.get_quest_completion_percentage(c, all_quests)
            print(f"Quest completion: {pct:.1f}%")
        except Exception:
            pass

def view_inventory():
    """List inventory and let player use/equip/drop items."""
    global current_character, all_items
    c = current_character
    inv = c.get("inventory", [])
    print("\n--- INVENTORY ---")
    if not inv:
        print("Inventory is empty.")
        return

    # Count items for display
    counts = {}
    for iid in inv:
        counts[iid] = counts.get(iid, 0) + 1

    for i, (iid, qty) in enumerate(counts.items(), start=1):
        name = all_items.get(iid, {}).get("name", iid)
        print(f"{i}) {name} (id:{iid}) x{qty}")

    print("\nOptions: 1) Use 2) Equip Weapon 3) Equip Armor 4) Drop 5) Back")
    choice = input("Choice: ").strip()
    if choice == "1":
        iid = input("Item id to use: ").strip()
        try:
            inventory_system.use_item(c, iid, all_items)
            print("Used", iid)
        except ItemNotFoundError:
            print("You do not have that item.")
        except InvalidItemTypeError:
            print("That item cannot be used.")
        except Exception as e:
            print("Could not use item:", e)
    elif choice == "2":
        iid = input("Weapon id to equip: ").strip()
        try:
            inventory_system.equip_weapon(c, iid, all_items)
            print("Equipped", iid)
        except ItemNotFoundError:
            print("You do not have that weapon.")
        except InvalidItemTypeError:
            print("That is not a weapon.")
        except Exception as e:
            print("Could not equip weapon:", e)
    elif choice == "3":
        iid = input("Armor id to equip: ").strip()
        try:
            inventory_system.equip_armor(c, iid, all_items)
            print("Equipped", iid)
        except ItemNotFoundError:
            print("You do not have that armor.")
        except InvalidItemTypeError:
            print("That is not armor.")
        except Exception as e:
            print("Could not equip armor:", e)
    elif choice == "4":
        iid = input("Item id to drop: ").strip()
        try:
            inventory_system.remove_item_from_inventory(c, iid)
            print("Dropped", iid)
        except ItemNotFoundError:
            print("You do not have that item.")
    else:
        return

def quest_menu():
    """Small quest manager UI: view, accept, abandon, complete (for testing)."""
    global current_character, all_quests
    c = current_character
    if not all_quests:
        print("No quests loaded.")
        return

    print("\n--- QUEST MENU ---")
    print("1) View Active Quests")
    print("2) View Available Quests")
    print("3) View Completed Quests")
    print("4) Accept Quest")
    print("5) Abandon Quest")
    print("6) Complete Quest (test)")
    print("7) Back")
    choice = input("Choice: ").strip()

    if choice == "1":
        active = quest_handler.get_active_quests(c, all_quests)
        if not active:
            print("No active quests.")
        else:
            quest_handler.display_quest_list(active)
    elif choice == "2":
        avail = quest_handler.get_available_quests(c, all_quests)
        if not avail:
            print("No available quests.")
        else:
            quest_handler.display_quest_list(avail)
    elif choice == "3":
        comp = quest_handler.get_completed_quests(c, all_quests)
        if not comp:
            print("No completed quests.")
        else:
            quest_handler.display_quest_list(comp)
    elif choice == "4":
        qid = input("Enter quest id to accept: ").strip()
        try:
            quest_handler.accept_quest(c, qid, all_quests)
            print("Quest accepted:", qid)
        except QuestNotFoundError:
            print("That quest does not exist.")
        except InsufficientLevelError:
            print("Your level is too low.")
        except QuestRequirementsNotMetError:
            print("Prerequisite not met.")
        except QuestAlreadyCompletedError:
            print("You already completed this quest.")
    elif choice == "5":
        qid = input("Enter quest id to abandon: ").strip()
        try:
            quest_handler.abandon_quest(c, qid)
            print("Quest abandoned:", qid)
        except QuestNotActiveError:
            print("That quest is not active.")
    elif choice == "6":
        qid = input("Enter quest id to complete: ").strip()
        try:
            rewards = quest_handler.complete_quest(c, qid, all_quests)
            print("Quest completed! Rewards:", rewards)
        except QuestNotFoundError:
            print("That quest not found.")
        except QuestNotActiveError:
            print("That quest is not active.")
    else:
        return

def explore():
    """Explore: find a random enemy and fight using combat_system."""
    global current_character
    c = current_character
    print("\n--- Exploring ---")
    # choose enemy based on level if helper exists, else fallback
    if hasattr(combat_system, "get_random_enemy_for_level"):
        enemy = combat_system.get_random_enemy_for_level(c.get("level",1))
    else:
        # fallback to goblin
        enemy = combat_system.create_enemy("goblin") if hasattr(combat_system, "create_enemy") else {"name":"Goblin","health":10,"max_health":10,"strength":2,"xp_reward":5,"gold_reward":2}
    print(f"A wild {enemy['name']} appears!")
    battle = combat_system.SimpleBattle(c, enemy)
    try:
        result = battle.start_battle()
        winner = result.get("winner")
        if winner == "player":
            # get rewards (function may vary)
            if hasattr(combat_system, "get_victory_rewards"):
                rewards = combat_system.get_victory_rewards(enemy)
            else:
                rewards = {"xp": enemy.get("xp_reward",0), "gold": enemy.get("gold_reward",0)}
            character_manager.gain_experience(c, rewards.get("xp",0))
            character_manager.add_gold(c, rewards.get("gold",0))
            print("Victory! You gained:", rewards)
        else:
            print("You were defeated...")
            handle_character_death()
    except Exception as e:
        print("Combat error:", e)

def shop():
    """Simple shop for buying and selling items from all_items."""
    global current_character, all_items
    c = current_character
    if not all_items:
        print("No items available in the shop.")
        return

    print("\n--- SHOP ---")
    ids = list(all_items.keys())
    for i, iid in enumerate(ids, start=1):
        item = all_items[iid]
        print(f"{i}) {item.get('name', iid)} - cost: {int(item.get('cost',0))} gold (id:{iid})")

    print(f"You have {c.get('gold',0)} gold.")
    print("1) Buy 2) Sell 3) Back")
    choice = input("Choice: ").strip()
    if choice == "1":
        iid = input("Enter item id to buy: ").strip()
        if iid not in all_items:
            print("Invalid id.")
            return
        try:
            inventory_system.purchase_item(c, iid, all_items)
            print("Purchased", iid)
        except InsufficientResourcesError:
            print("Not enough gold.")
        except InventoryFullError:
            print("Inventory full.")
        except Exception as e:
            print("Could not purchase:", e)
    elif choice == "2":
        iid = input("Enter item id to sell: ").strip()
        if iid not in all_items:
            print("Invalid id.")
            return
        try:
            amount = inventory_system.sell_item(c, iid, all_items)
            print("Sold", iid, "for", amount, "gold.")
        except ItemNotFoundError:
            print("You do not have that item.")
        except Exception as e:
            print("Could not sell:", e)
    else:
        return

# ---------------------------
# Save/load and death handling
# ---------------------------

def save_game():
    """Save current character state to disk."""
    global current_character
    if current_character is None:
        print("No active character.")
        return
    try:
        ok = character_manager.save_character(current_character)
        if ok:
            print("Game saved.")
    except Exception as e:
        print("Saving failed:", e)

def load_game_data():
    """
    Load quests and items into global variables.
    If load fails, return False so caller can create defaults if available.
    """
    return safe_load_data()

def handle_character_death():
    """Offer revive option or return to main menu."""
    global current_character, game_running
    c = current_character
    print("\n--- You died ---")
    print("1) Revive for 50 gold")
    print("2) Quit to main menu")
    choice = input("Choose 1-2: ").strip()
    if choice == "1":
        cost = 50
        if c.get("gold",0) >= cost:
            try:
                character_manager.add_gold(c, -cost)
                character_manager.revive_character(c)
                print("You have been revived.")
            except Exception as e:
                print("Could not revive:", e)
                game_running = False
        else:
            print("Not enough gold. Returning to main menu.")
            game_running = False
    else:
        print("Returning to main menu.")
        game_running = False

# ---------------------------
# Program entry point
# ---------------------------

def main():
    """Start program: load data, then show main menu loop."""
    display_welcome()
    # try to load data; if fails and create function exists, use it
    ok = load_game_data()
    if not ok:
        # try to create default data if module has function
        if hasattr(game_data, "create_default_data_files"):
            print("Creating default data files...")
            try:
                game_data.create_default_data_files()
                load_game_data()
            except Exception as e:
                print("Failed to create default data:", e)
                return
        else:
            print("Game data missing and no default creator. Exiting.")
            return

    # main loop
    while True:
        choice = main_menu()
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("Goodbye!")
            break

def display_welcome():
    print("="*50)
    print("   QUEST CHRONICLES - SIMPLE RPG (FRESHMAN-LEVEL)")
    print("="*50)
    print("Welcome! Create a hero, complete quests, and explore.")
    print()

if __name__ == "__main__":
    main()
