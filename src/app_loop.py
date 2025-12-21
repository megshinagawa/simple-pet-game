"""
Game loop and action handling for the pet game.
"""
import os
from src.pet import Pet
from src.user import User
from src.config import FOODS, MAX_STAT, PETS_PATH
from src.data_handler import save_pet, load_pet, save_user
from src.ui import display_action_menu, display_food_menu, display_pet_status, display_game_menu
from src.games.which_way import play_which_way


def initialize_pet(user, pet_filename=None):
    """
    Initialize or load a pet for the user.

    Args:
        user (User): The user who owns the pet
        pet_filename (str, optional): Specific pet filename to load

    Returns:
        tuple[Pet, str]: Pet instance and the filename it should be saved to
    """
    # Determine which pet to load
    filename = None
    if pet_filename:
        # Specific pet file was requested
        filename = os.path.join(PETS_PATH, pet_filename)
        # Add to user's collection if not already there
        if not any(pet['filename'] == pet_filename for pet in user.pets):
            user.add_pet(pet_filename)
            save_user(user)
    elif user.current_pet:
        # Load user's current pet (current_pet is now a filename)
        pet_filename = user.current_pet
        filename = os.path.join(PETS_PATH, user.current_pet)

    # Load or create pet
    if filename:
        loaded_pet = load_pet(filename)
        if loaded_pet:
            print(f"Loading {loaded_pet.name}...")
            loaded_pet.update_stats()
            return loaded_pet, filename
        else:
            # File exists but couldn't load - create new pet
            print("Could not load pet file. Creating new pet...")
            pet = create_new_pet(user)

            # Use the existing pet_filename if it was set
            if not pet_filename:
                pet_filename = f"{pet.name.lower().replace(' ', '_')}.json"
                filename = os.path.join(PETS_PATH, pet_filename)

            # Add pet to user's collection
            if not any(p['filename'] == pet_filename for p in user.pets):
                user.add_pet(pet_filename, pet.name)
                save_user(user)

            return pet, filename
    else:
        # Create new pet (no existing pet to load)
        pet = create_new_pet(user)

        # Generate pet filename
        pet_filename = f"{pet.name.lower().replace(' ', '_')}.json"
        filename = os.path.join(PETS_PATH, pet_filename)

        # Add pet to user's collection
        if not any(p['filename'] == pet_filename for p in user.pets):
            user.add_pet(pet_filename, pet.name)
            save_user(user)

        return pet, filename


def create_new_pet(user):
    """
    Create a new pet by prompting for name.

    Args:
        user (User): The user who will own the pet

    Returns:
        Pet: Newly created pet instance
    """
    while True:
        pet_name = input("What would you like to name your pet? ").strip()
        if pet_name:
            break
        print("Pet name cannot be empty. Please try again.")

    return Pet(pet_name, owner=user.username)


def handle_view_status(pet):
    """
    Handle the 'View pet status' action.

    Args:
        pet (Pet): The pet to display
    """
    display_pet_status(pet)


def handle_feed_pet(pet):
    """
    Handle the 'Feed pet' action.

    Args:
        pet (Pet): The pet to feed

    Returns:
        bool: True if feeding was successful, False otherwise
    """
    # Check if pet can eat before showing food menu
    if pet.fullness >= MAX_STAT:
        print(f"\n>> {pet.name} is already full!")
        return False
    if pet.sleep:
        print(f"\n>> {pet.name} is sleeping and can't eat right now!")
        return False

    display_food_menu()
    try:
        food = int(input(f"Which food would you like to feed {pet.name}? ").strip())
    except ValueError:
        print("\n>> Please enter a valid number.")
        return False

    if food in FOODS:
        food_data = FOODS[food]
        pet.feed(food_data['fill_value'])
        print(f"\n>> {pet.name} ate a {food_data['name'].lower()}!")
        print(f">> {pet.name} is at {int(pet.fullness)}% fullness!")
        return True
    else:
        print("\n>> Invalid food selection!")
        return False


def handle_sleep(pet):
    """
    Handle the 'Go to bed' action.

    Args:
        pet (Pet): The pet to put to sleep

    Returns:
        bool: True if action was successful, False otherwise
    """
    if pet.sleep:
        print(f"\n>> {pet.name} is sleeping already!")
        return False
    else:
        pet.go_to_bed()
        print(f"\n>> {pet.name} is now sleeping!")
        return True


def handle_wake_up(pet):
    """
    Handle the 'Wake up' action.

    Args:
        pet (Pet): The pet to wake up

    Returns:
        bool: True if action was successful, False otherwise
    """
    if not pet.sleep:
        print(f"\n>> {pet.name} is not sleeping!")
        return False
    else:
        pet.wake_up()
        print(f"\n>> {pet.name} is at {int(pet.energy)}% energy!")
        return True


def handle_user_display(user):
    """
    Handle the user settings sub-menu.

    Args:
        user (User): The current user

    Returns:
        bool: False if user wants to exit the game, True otherwise
    """
    print("\n" + "-" * 50)
    print(f"Username: {user.username}")
    print(f"Birthday: {user.birthday}")
    current_pet_name = user.get_current_pet_name()
    print(f"Current pet: {current_pet_name if current_pet_name else 'None'}")
    print(f"Total pets owned: {len(user.pets)}")
    pet_names = [pet['name'] for pet in user.pets]
    print(f"Pets: {', '.join(pet_names) if pet_names else 'None'}")
    print(f"Games played: {user.games_played}")
    print(f"Games won: {user.games_won}")
    print(f"Win rate: {user.get_win_rate():.1f}%")
    print("-" * 50)
    return True


def handle_play_games(pet, user):
    """
    Handle the 'Play games' action.
    
    Args:
        pet (Pet): The current pet
        user (User): The current user
        
    Returns:
        bool: True if continuing game loop, False to exit
    """
    if pet.sleep:
        print(f"{pet.name} is sleeping and can't play games!")
        return True

    while True:
        display_game_menu()
        
        try:
            choice = int(input("\nWhich game would you like to play? ").strip())
        except ValueError:
            print("\n>> Please enter a valid number.")
            continue
        
        if choice == 1:
            win_status = play_which_way(pet)
            user.update_game_stats(win_status)
        elif choice == 2:
            print("Memory game coming soon!")
        elif choice == 3:
            print("Coming soon!")
        elif choice == 4:
            return True  # Back to main menu
        else:
            print("\n>> Invalid choice!")


def run_game_loop(user, pet, pet_filename):
    """
    Run the main game loop.

    Args:
        user (User): The current user
        pet (Pet): The pet being cared for
        pet_filename (str): The filename to save the pet to
    """
    if user.is_birthday_today():
        print()
        print("*" * 50)
        print("It's your birthday!")
        print(f"{(pet.name)} wishes you a happy birthday!")
        print("*" * 50)

    while True:
        display_action_menu()

        try:
            user_input = int(input("\nWhat would you like to do? ").strip())
        except ValueError:
            print("\n>> Please enter a valid number.")
            continue

        if user_input == 1:
            handle_view_status(pet)
        elif user_input == 2:
            handle_feed_pet(pet)
        elif user_input == 3:
            handle_sleep(pet)
        elif user_input == 4:
            handle_wake_up(pet)
        elif user_input == 5:
            handle_play_games(pet, user)
        elif user_input == 6:
            handle_user_display(user)
        elif user_input == 7:
            print("=" * 50)
            save_pet(pet, pet_filename)
            save_user(user)
            print("Good Bye!")
            print("=" * 50)
            break
        else:
            print("\n>> Please enter a valid number.")
