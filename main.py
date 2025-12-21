import json
import os
import sys
from src.pet import Pet
from src.user import User
from src.config import PET_DATA_PATH, FOODS, MAX_STAT, PETS_PATH, USERS_PATH

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


def save_game(pet, filename = PET_DATA_PATH):
    """Save pet data to file"""
    # Extract and create directory if needed
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(pet.to_dict(), f, indent=2)
    print(f"Game saved to {filename}!")


def load_game(filename = PET_DATA_PATH):
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


def save_user(user, username=None):
    """Save user data to file"""
    if username is None:
        username = user.username

    # Create user filename based on username
    filename = os.path.join(USERS_PATH, f"{username}.json")

    # Create directory if needed
    os.makedirs(USERS_PATH, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(user.to_dict(), f, indent=2)


def load_user(username):
    """Load user data from file"""
    filename = os.path.join(USERS_PATH, f"{username}.json")
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return User.from_dict(data)
    except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
        print(f"Error loading user file: {e}")
        return None


def list_users():
    """List all available users"""
    if not os.path.exists(USERS_PATH):
        return []

    users = []
    for filename in os.listdir(USERS_PATH):
        if filename.endswith('.json'):
            username = filename[:-5]  # Remove .json extension
            users.append(username)
    return users


def main(username=None, pet_filename=None):
    """
    Main game loop
    Args:
        username (str, optional): Username to login/create
        pet_filename (str, optional): Specific pet filename to load
    """
    print("=" * 50)
    print("WELCOME!")
    print("=" * 50)

    # User login/creation
    user: User
    if username:
        # Try to load existing user
        loaded_user = load_user(username)
        if loaded_user:
            user = loaded_user

            # Update login streak
            streak_continued, days_since = user.update_login_streak(user.last_login_date)
            user.last_login_date = user.birthday.today()

            print(f"Welcome back, {user.username}!")

            # Show streak message
            if days_since == 0:
                print(f"You've already logged in today! Current streak: {user.current_login_streak} days")
            elif streak_continued:
                print(f"Login streak continues! Current streak: {user.current_login_streak} days")
                if user.current_login_streak == user.longest_login_streak:
                    print("New record!")
            else:
                print(f"Streak broken! But everyday is a new start: {user.current_login_streak} day")

        else:
            print(f"Creating new user: {username}")
            while True:
                birthday = input("Enter your birthday (YYYY-MM-DD): ").strip()
                try:
                    user = User(username, birthday)
                    break
                except (ValueError, TypeError) as e:
                    print(f"Invalid birthday format: {e}")
                    print("Please try again.")
            save_user(user)
    else:
        # List existing users
        existing_users = list_users()
        if existing_users:
            print("\nExisting users:")
            for i, u in enumerate(existing_users, 1):
                print(f"{i}. {u}")
            print(f"{len(existing_users) + 1}. Create new user")

            try:
                choice = int(input("\nSelect a user (enter number): ").strip())
                if 1 <= choice <= len(existing_users):
                    username = existing_users[choice - 1]
                    loaded_user = load_user(username)
                    if loaded_user:
                        user = loaded_user

                        # Update login streak
                        streak_continued, days_since = user.update_login_streak(user.last_login_date)
                        user.last_login_date = user.birthday.today()

                        age = (user.birthday.today() - user.birthday).days // 365
                        print(f"Welcome back, {user.username}! (Age: {age})")

                        # Show streak message
                        if days_since == 0:
                            print(f"You've already logged in today! Current streak: {user.current_login_streak} days")
                        elif streak_continued:
                            print(f"Login streak continues! Current streak: {user.current_login_streak} days")
                            if user.current_login_streak == user.longest_login_streak:
                                print("New record!")
                        else:
                            print(f"Streak broken! You missed {days_since - 1} day(s). Starting fresh: {user.current_login_streak} day")
                            if user.longest_login_streak > 1:
                                print(f"Your longest streak was: {user.longest_login_streak} days")
                    else:
                        # Fallback if file exists but can't be loaded
                        print(f"Error loading user {username}. Creating new user.")
                        while True:
                            birthday = input("Enter your birthday (YYYY-MM-DD): ").strip()
                            try:
                                user = User(username, birthday)
                                break
                            except (ValueError, TypeError) as e:
                                print(f"Invalid birthday format: {e}")
                                print("Please try again.")
                        save_user(user)
                else:
                    username = input("Enter new username: ").strip()
                    while True:
                        birthday = input("Enter your birthday (YYYY-MM-DD): ").strip()
                        try:
                            user = User(username, birthday)
                            break
                        except (ValueError, TypeError) as e:
                            print(f"Invalid birthday format: {e}")
                            print("Please try again.")
                    save_user(user)
                    print(f"Created new user: {username}")
            except (ValueError, IndexError):
                print("Invalid selection. Creating new user...")
                username = input("Enter username: ").strip()
                while True:
                    birthday = input("Enter your birthday (YYYY-MM-DD): ").strip()
                    try:
                        user = User(username, birthday)
                        break
                    except (ValueError, TypeError) as e:
                        print(f"Invalid birthday format: {e}")
                        print("Please try again.")
                save_user(user)
        else:
            username = input("Enter username: ").strip()
            while True:
                birthday = input("Enter your birthday (YYYY-MM-DD): ").strip()
                try:
                    user = User(username, birthday)
                    break
                except (ValueError, TypeError) as e:
                    print(f"Invalid birthday format: {e}")
                    print("Please try again.")
            save_user(user)
            print(f"Created new user: {username}")

    # Determine which pet to load
    filename: str | None
    if pet_filename:
        # Specific pet file was requested
        filename = os.path.join(PETS_PATH, pet_filename)
        # Add to user's collection if not already there
        if pet_filename not in user.pets:
            user.add_pet(pet_filename)
            save_user(user)
    elif user.current_pet:
        # Load user's current pet
        pet_filename = user.current_pet
        filename = os.path.join(PETS_PATH, user.current_pet)
    else:
        # No current pet, will create a new one
        pet_filename = None
        filename = None  # Will be set when creating new pet

    # Load or create pet
    pet: Pet
    if filename:
        loaded_pet = load_game(filename)
        if loaded_pet:
            pet = loaded_pet
            print(f"Loading {pet.name}...")
            pet.update_stats()
        else:
            # File exists but couldn't load - create new pet
            print("Could not load pet file. Creating new pet...")
            while True:
                pet_name = input("What would you like to name your pet? ").strip()
                if pet_name:
                    break
                print("Pet name cannot be empty. Please try again.")

            pet = Pet(pet_name, owner=user.username)

            # Use the existing pet_filename if it was set
            if not pet_filename:
                pet_filename = f"{pet_name.lower().replace(' ', '_')}.json"
                filename = os.path.join(PETS_PATH, pet_filename)

            # Add pet to user's collection
            if pet_filename not in user.pets:
                user.add_pet(pet_filename)
                save_user(user)
    else:
        # Create new pet (no existing pet to load)
        while True:
            pet_name = input("What would you like to name your pet? ").strip()
            if pet_name:
                break
            print("Pet name cannot be empty. Please try again.")

        pet = Pet(pet_name, owner=user.username)

        # Generate pet filename
        if not pet_filename:
            pet_filename = f"{pet_name.lower().replace(' ', '_')}.json"

        filename = os.path.join(PETS_PATH, pet_filename)

        # Add pet to user's collection
        if pet_filename not in user.pets:
            user.add_pet(pet_filename)
            save_user(user)

    # Ensure filename is always set before entering game loop
    if filename is None:
        raise RuntimeError("Filename not set - this should never happen")

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
                print(f">> {pet.name} is at {int(pet.fullness)}% fullness!")
            else:
                print("\n>> Invalid food selection!")
        elif user_input == 3:
            if pet.sleep:
                print(f"\n>> {pet.name} is sleeping already!")
            else:
                pet.go_to_bed()
                print(f"\n>> {pet.name} is now sleeping!")
        elif user_input == 4:
            if not pet.sleep:
                print(f"\n>> {pet.name} is not sleeping!")
            else:
                pet.wake_up()
                print(f"\n>> {pet.name} is at {int(pet.energy)}% energy!")
        elif user_input == 5:
            print("=" * 50)
            save_game(pet, filename)
            save_user(user)
            print("Good Bye!")
            print("=" * 50)
            break
        else:
            print("\n>> Please enter a valid number.")


if __name__ == "__main__":
    # Parse command-line arguments
    # Usage: python main.py [username] [pet_filename]
    username_arg = sys.argv[1] if len(sys.argv) > 1 else None
    pet_file_arg = sys.argv[2] if len(sys.argv) > 2 else None
    main(username_arg, pet_file_arg)