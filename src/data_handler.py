"""
Persistence layer for saving and loading game data.
"""
import json
import os
from src.pet import Pet
from src.user import User
from src.config import PET_DATA_PATH, USERS_PATH, PETS_PATH


def save_pet(pet, filename=PET_DATA_PATH):
    """
    Save pet data to file.

    Args:
        pet (Pet): Pet instance to save
        filename (str): Path to save file
    """
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(pet.to_dict(), f, indent=2)
    print(f"Game saved to {filename}!")


def load_pet(filename=PET_DATA_PATH):
    """
    Load pet data from file.

    Args:
        filename (str): Path to save file

    Returns:
        Pet | None: Loaded Pet instance or None if file doesn't exist or is invalid
    """
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
    """
    Save user data to file.

    Args:
        user (User): User instance to save
        username (str, optional): Override username for filename
    """
    if username is None:
        username = user.username

    filename = os.path.join(USERS_PATH, f"{username}.json")
    os.makedirs(USERS_PATH, exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(user.to_dict(), f, indent=2)


def load_user(username):
    """
    Load user data from file.

    Args:
        username (str): Username to load

    Returns:
        User | None: Loaded User instance or None if file doesn't exist or is invalid
    """
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
    """
    List all available users.

    Returns:
        list[str]: List of usernames
    """
    if not os.path.exists(USERS_PATH):
        return []

    users = []
    for filename in os.listdir(USERS_PATH):
        if filename.endswith('.json'):
            username = filename[:-5]  # Remove .json extension
            users.append(username)
    return users
