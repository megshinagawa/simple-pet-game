"""
Simple Pet Game - Main entry point.

A command-line virtual pet game where you care for your pet by feeding it
and managing its sleep schedule.
"""
import sys
from src.auth import authenticate_user
from src.app_loop import initialize_pet, run_game_loop
from src.ui import display_welcome
from src.data_handler import save_user


def main(username=None, pet_filename=None):
    """
    Main game entry point.

    Args:
        username (str, optional): Username to login/create
        pet_filename (str, optional): Specific pet filename to load
    """
    display_welcome()

    # Authenticate user
    user = authenticate_user(username)
    save_user(user)

    # Initialize pet
    pet, filename = initialize_pet(user, pet_filename)

    # Run game loop
    run_game_loop(user, pet, filename)


if __name__ == "__main__":
    # Parse command-line arguments
    # Usage: python main.py [username] [pet_filename]
    username_arg = sys.argv[1] if len(sys.argv) > 1 else None
    pet_file_arg = sys.argv[2] if len(sys.argv) > 2 else None
    main(username_arg, pet_file_arg)
