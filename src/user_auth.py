"""
User authentication and management.
"""
from src.user import User
from src.data_handler import load_user, save_user, list_users


def show_login_streak_message(user, streak_continued, days_since):
    """
    Display login streak message based on user's streak status.

    Args:
        user (User): User instance
        streak_continued (bool): Whether the streak continued
        days_since (int): Days since last login
    """
    if days_since == 0:
        print(f"Current streak: {user.current_login_streak} days")
    elif streak_continued:
        print(f"Login streak updated! Current streak: {user.current_login_streak} days")
        if user.current_login_streak == user.longest_login_streak:
            print(">> New record!")
    else:
        print("Glad to have you back!")
        print(f">> It's been {days_since - 1} day(s) since your last login!")


def create_new_user(username):
    """
    Create a new user by prompting for birthday.

    Args:
        username (str): Username for the new user

    Returns:
        User: Newly created user instance
    """
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
    return user


def login_existing_user(username):
    """
    Login an existing user and update their login streak.

    Args:
        username (str): Username to login

    Returns:
        User | None: User instance if successful, None if user doesn't exist
    """
    loaded_user = load_user(username)
    if not loaded_user:
        return None

    # Update login streak
    streak_continued, days_since = loaded_user.update_login_streak(loaded_user.last_login_date)
    loaded_user.last_login_date = loaded_user.birthday.today()

    print(f"Welcome back, {loaded_user.username}!")

    # Show streak message
    show_login_streak_message(loaded_user, streak_continued, days_since)

    return loaded_user


def select_user_from_list():
    """
    Display list of users and prompt for selection or new user creation.

    Returns:
        User: Selected or newly created user instance
    """
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
                user = login_existing_user(username)
                if user:
                    return user
                # Fallback if file exists but can't be loaded
                print(f"Error loading user {username}. Creating new user.")
                return create_new_user(username)
            else:
                username = input("Enter new username: ").strip()
                return create_new_user(username)
        except (ValueError, IndexError):
            print("Invalid selection. Creating new user...")
            username = input("Enter username: ").strip()
            return create_new_user(username)
    else:
        username = input("Enter username: ").strip()
        return create_new_user(username)


def authenticate_user(username=None):
    """
    Authenticate or create a user.

    Args:
        username (str, optional): Username to login/create. If None, prompts for selection.

    Returns:
        User: Authenticated or newly created user instance
    """
    if username:
        # Try to load existing user
        loaded_user = load_user(username)
        if loaded_user:
            # Update login streak
            streak_continued, days_since = loaded_user.update_login_streak(loaded_user.last_login_date)
            loaded_user.last_login_date = loaded_user.birthday.today()

            print(f"Welcome back, {loaded_user.username}!")
            show_login_streak_message(loaded_user, streak_continued, days_since)

            return loaded_user
        else:
            return create_new_user(username)
    else:
        return select_user_from_list()
