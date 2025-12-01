"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

import character_manager


# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")

    quest = quest_data_dict[quest_id]

    # Already completed?
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed")

    # Already active?
    if quest_id in character["active_quests"]:
        raise QuestRequirementsNotMetError("Quest already active")

    # Level requirement
    if character["level"] < quest["required_level"]:
        raise InsufficientLevelError("Level too low to accept quest")

    # Prerequisite requirement
    prereq = quest["prerequisite"]
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError("Prerequisite quest not completed")

    character["active_quests"].append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")

    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active")

    quest = quest_data_dict[quest_id]

    # Remove from active, add to completed
    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)

    # Rewards
    xp = quest["reward_xp"]
    gold = quest["reward_gold"]

    character_manager.gain_experience(character, xp)
    character_manager.add_gold(character, gold)

    return {"xp": xp, "gold": gold}


def abandon_quest(character, quest_id):
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest not active")

    character["active_quests"].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    return [quest_data_dict[q] for q in character["active_quests"] if q in quest_data_dict]


def get_completed_quests(character, quest_data_dict):
    return [quest_data_dict[q] for q in character["completed_quests"] if q in quest_data_dict]


def get_available_quests(character, quest_data_dict):
    available = []

    for qid, data in quest_data_dict.items():
        # skip completed
        if qid in character["completed_quests"]:
            continue
        # skip active
        if qid in character["active_quests"]:
            continue
        # level
        if character["level"] < data["required_level"]:
            continue
        # prerequisite
        prereq = data["prerequisite"]
        if prereq != "NONE" and prereq not in character["completed_quests"]:
            continue

        available.append(data)

    return available


# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character["completed_quests"]


def is_quest_active(character, quest_id):
    return quest_id in character["active_quests"]


def can_accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        return False

    data = quest_data_dict[quest_id]

    if quest_id in character["completed_quests"]:
        return False
    if quest_id in character["active_quests"]:
        return False
    if character["level"] < data["required_level"]:
        return False

    prereq = data["prerequisite"]
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError("Quest not found")

    chain = []
    current = quest_id

    while True:
        if current not in quest_data_dict:
            raise QuestNotFoundError("Invalid prerequisite chain")

        chain.append(current)

        prereq = quest_data_dict[current]["prerequisite"]
        if prereq == "NONE":
            break

        current = prereq

    return chain[::-1]  # earliest to latest


# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    total = len(quest_data_dict)
    if total == 0:
        return 0.0
    completed = len(character["completed_quests"])
    return (completed / total) * 100


def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = 0
    total_gold = 0

    for qid in character["completed_quests"]:
        if qid in quest_data_dict:
            total_xp += quest_data_dict[qid]["reward_xp"]
            total_gold += quest_data_dict[qid]["reward_gold"]

    return {"total_xp": total_xp, "total_gold": total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    return [
        quest
        for quest in quest_data_dict.values()
        if min_level <= quest["required_level"] <= max_level
    ]


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Required Level: {quest_data['required_level']}")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    print(f"Reward XP: {quest_data['reward_xp']}")
    print(f"Reward Gold: {quest_data['reward_gold']}")
    print()


def display_quest_list(quest_list):
    for q in quest_list:
        print(f"- {q['title']} (Level {q['required_level']}) — XP: {q['reward_xp']} Gold: {q['reward_gold']}")


def display_character_quest_progress(character, quest_data_dict):
    pct = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print(f"Active Quests: {len(character['active_quests'])}")
    print(f"Completed Quests: {len(character['completed_quests'])}")
    print(f"Completion: {pct:.2f}%")
    print(f"Total XP Earned from Quests: {rewards['total_xp']}")
    print(f"Total Gold Earned from Quests: {rewards['total_gold']}")


# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    for qid, quest in quest_data_dict.items():
        prereq = quest["prerequisite"]
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite '{prereq}' for quest '{qid}' does not exist")
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

