"""
Menu display functions for the pet game UI.
"""
from src.config import FOODS


def display_action_menu():
    """Display action menu"""
    print("\n" + "=" * 50)
    print("ACTIONS")
    print("=" * 50)
    print("1. View pet status")
    print("2. Feed pet")
    print("3. Go to bed")
    print("4. Wake up")
    print("5. Play games")
    print("6. Check user info")
    print("7. Save and exit")
    print("=" * 50)


def display_food_menu():
    """Display food menu"""
    print("\n" + "-" * 50)
    print("FOOD MENU")
    print("-" * 50)
    for food_id, food_data in FOODS.items():
        print(f"{food_id}. {food_data['name']} (+{food_data['fill_value']} fullness)")
    print("-" * 50)


def display_welcome():
    """Display welcome banner"""
    print("=" * 50)
    print("WELCOME!")
    print("=" * 50)


def display_pet_status(pet):
    """Display pet status in formatted view"""
    pet.update_stats()
    print("\n" + "=" * 50)
    print("PET STATUS")
    print("=" * 50)
    print(pet)
    print("=" * 50)
