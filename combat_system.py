"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError,
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    enemy_type = enemy_type.lower()

    if enemy_type == "goblin":
        return {
            "name": "Goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        }
    elif enemy_type == "orc":
        return {
            "name": "Orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        }
    elif enemy_type == "dragon":
        return {
            "name": "Dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    else:
        raise InvalidTargetError("Unknown enemy type")


def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# BATTLE SYSTEM
# ============================================================================

class SimpleBattle:
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turns = 0

    def start_battle(self):
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is already dead")

        while self.combat_active:
            winner = self.check_battle_end()
            if winner:
                if winner == "player":
                    xp = self.enemy["xp_reward"]
                    gold = self.enemy["gold_reward"]
                    self.character["xp"] += xp
                    self.character["gold"] += gold
                    return {"winner": "player", "xp_gained": xp, "gold_gained": gold}
                else:
                    return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

            # player turn
            self.player_turn()

            # check end again
            if self.check_battle_end():
                continue

            # enemy turn
            self.enemy_turn()

        return {"winner": "escape", "xp_gained": 0, "gold_gained": 0}

    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Battle is not active")

        # For automated tests, we don’t actually prompt the user.
        # We simulate a basic attack every time.
        damage = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, damage)

    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError("Battle is not active")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)

    def calculate_damage(self, attacker, defender):
        dmg = attacker["strength"] - (defender["strength"] // 4)
        return max(1, dmg)

    def apply_damage(self, target, damage):
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0

    def check_battle_end(self):
        if self.enemy["health"] <= 0:
            self.combat_active = False
            return "player"
        if self.character["health"] <= 0:
            self.combat_active = False
            return "enemy"
        return None

    def attempt_escape(self):
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    # No cooldown system for now — simple version
    job = character["class"].lower()

    if job == "warrior":
        return warrior_power_strike(character, enemy)
    elif job == "mage":
        return mage_fireball(character, enemy)
    elif job == "rogue":
        return rogue_critical_strike(character, enemy)
    elif job == "cleric":
        return cleric_heal(character)
    else:
        raise InvalidTargetError("Class has no special ability")


def warrior_power_strike(character, enemy):
    dmg = character["strength"] * 2
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Warrior used Power Strike for {dmg} damage!"


def mage_fireball(character, enemy):
    dmg = character["magic"] * 2
    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Mage cast Fireball for {dmg} damage!"


def rogue_critical_strike(character, enemy):
    if random.random() < 0.5:
        dmg = character["strength"] * 3
    else:
        dmg = character["strength"]

    enemy["health"] -= dmg
    if enemy["health"] < 0:
        enemy["health"] = 0
    return f"Rogue dealt {dmg} damage!"


def cleric_heal(character):
    character["health"] += 30
    if character["health"] > character["max_health"]:
        character["health"] = character["max_health"]
    return "Cleric healed 30 HP!"


# ============================================================================
# UTILITIES
# ============================================================================

def can_character_fight(character):
    return character["health"] > 0 and not character.get("in_battle", False)


def get_victory_rewards(enemy):
    return {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}


def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: {character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: {enemy['health']}/{enemy['max_health']}")


def display_battle_log(message):
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

