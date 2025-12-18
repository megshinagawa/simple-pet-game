import json
import os
from src.pet import Pet
from src.config import SAVE_FILENAME, FOODS, MAX_STAT

def display_action_menu():
    """Display action menu"""
    print("\n" + "=" * 50)
    print("ACTIONS")
    print("=" * 50)
    print("1. View pet status")
    print("2. Feed pet")
    print("3. Go to bed")
    print("4. Wake up")
    print("5. Save and exit")
    print("=" * 50)


def display_food_menu():
    """Display food menu"""
    print("\n" + "-" * 50)
    print("FOOD MENU")
    print("-" * 50)
    for food_id, food_data in FOODS.items():
        print(f"{food_id}. {food_data['name']} (+{food_data['fill_value']} fullness)")
    print("-" * 50)


def save_game(pet, filename = SAVE_FILENAME):
    """Save pet data to file"""
    # Extract and create directory if needed
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(pet.to_dict(), f, indent=2)
    print(f"Game saved to {filename}!")


def load_game(filename = SAVE_FILENAME):
    """Load pet data from file"""
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Pet.from_dict(data)
    except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
        print(f"Error loading save file: {e}")
        print("Starting with a new pet instead.")
        return None


def main():
    """
    Docstring for main
    """
    print("=" * 50)
    print("WELCOME!")
    print("=" * 50)

    pet = load_game()
    if pet:
        print(f"Welcome back! Loading {pet.name}...")
        pet.update_stats()  # Update stats for time passed since last play
    else:
        while True:
            pet_name = input("What would you like to name your pet? ").strip()
            if pet_name:
                break
            print("Pet name cannot be empty. Please try again.")
        pet = Pet(pet_name)

    while True:
        display_action_menu()

        try:
            user_input = int(input("\nWhat would you like to do? ").strip())
        except ValueError:
            print("\n>> Please enter a valid number.")
            continue

        if user_input == 1:
            pet.update_stats()  # Update stats before displaying
            print("\n" + "=" * 50)
            print("PET STATUS")
            print("=" * 50)
            print(pet)
            print("=" * 50)
        elif user_input == 2:
            # Check if pet can eat before showing food menu
            if pet.fullness >= MAX_STAT:
                print(f"\n>> {pet.name} is already full!")
                continue
            if pet.sleep:
                print(f"\n>> {pet.name} is sleeping and can't eat right now!")
                continue

            display_food_menu()
            try:
                food = int(input(f"Which food would you like to feed {pet.name}? ").strip())
            except ValueError:
                print("\n>> Please enter a valid number.")
                continue

            if food in FOODS:
                food_data = FOODS[food]
                pet.feed(food_data['fill_value'])
                print(f"\n>> {pet.name} ate a {food_data['name'].lower()}!")
            else:
                print("\n>> Invalid food selection!")
        elif user_input == 3:
            if pet.sleep:
                print(f"\n>> {pet.name} is sleeping already!")
            else:
                pet.go_to_bed()
                print("\n" + "=" * 50)
                print("PET STATUS")
                print("=" * 50)
                print(pet)
                print("=" * 50)
        elif user_input == 4:
            if not pet.sleep:
                print(f"\n>> {pet.name} is not sleeping!")
            else:
                pet.wake_up()
                print("\n" + "=" * 50)
                print("PET STATUS")
                print("=" * 50)
                print(pet)
                print("=" * 50)
        elif user_input == 5:
            print("=" * 50)
            save_game(pet)
            print("Good Bye!")
            print("=" * 50)
            break
        else:
            print("\n>> Please enter a valid number.")
        

if __name__ == "__main__":
    main()