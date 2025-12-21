import datetime


class User:
    """
    A user who can own multiple pets.

    Attributes:
        username (str): The user's username
        birthday (datetime.date): The user's birthday
        pets (list): List of pet dictionaries with 'name' and 'filename' keys
        current_pet (str | None): Currently active pet's filename (e.g., 'fluffy_cat.json')
    """

    def __init__(self, username, birthday=None):
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if len(username) > 50:
            raise ValueError("Username cannot exceed 50 characters")
        self.username = username.strip()

        # Set birthday - default to today if not provided
        if birthday is None:
            self.birthday = datetime.datetime.now().date()
        elif isinstance(birthday, datetime.date):
            self.birthday = birthday
        elif isinstance(birthday, str):
            self.birthday = datetime.date.fromisoformat(birthday)
        else:
            raise TypeError("Birthday must be a datetime.date, string, or None")
        
        # Set first log-in anniversary date
        self.first_login_date = datetime.datetime.now().date()
        self.last_login_date = datetime.datetime.now().date()

        # Set stats
        self.longest_login_streak = 0
        self.current_login_streak = 1

        # Pet ownership tracking
        # Each pet entry is a dict: {'name': str, 'filename': str}
        self.pets = []  # List of pet dictionaries
        self.current_pet = None  # Currently active pet filename

    def add_pet(self, pet_filename, pet_name=None):
        """
        Add a pet to this user's collection.
        Args:
            pet_filename (str): Filename of the pet to add (e.g., 'fluffy_cat.json')
            pet_name (str, optional): Display name of the pet. If not provided,
                                     derived from filename by removing .json and replacing _ with spaces
        """
        if not isinstance(pet_filename, str):
            raise TypeError("Pet filename must be a string")
        if not pet_filename.strip():
            raise ValueError("Pet filename cannot be empty")

        pet_filename = pet_filename.strip()

        # Derive pet name from filename if not provided
        if pet_name is None:
            pet_name = pet_filename.replace('.json', '').replace('_', ' ')

        # Check if pet already exists (by filename)
        if not any(pet['filename'] == pet_filename for pet in self.pets):
            self.pets.append({'name': pet_name, 'filename': pet_filename})
            # Set as current pet if it's the first one
            if self.current_pet is None:
                self.current_pet = pet_filename

    def remove_pet(self, pet_filename):
        """
        Remove a pet from this user's collection.
        Args:
            pet_filename (str): Filename of the pet to remove
        """
        # Find and remove pet by filename
        self.pets = [pet for pet in self.pets if pet['filename'] != pet_filename]

        # Clear current pet if it was the one removed
        if self.current_pet == pet_filename:
            self.current_pet = self.pets[0]['filename'] if self.pets else None

    def set_current_pet(self, pet_filename):
        """
        Set the currently active pet.
        Args:
            pet_filename (str): Filename of the pet to set as current
        """
        if not any(pet['filename'] == pet_filename for pet in self.pets):
            raise ValueError(f"Pet with filename '{pet_filename}' is not owned by this user")
        self.current_pet = pet_filename

    def get_current_pet_name(self):
        """
        Get the display name of the current pet.
        Returns:
            str | None: The pet's display name, or None if no current pet
        """
        if self.current_pet is None:
            return None
        for pet in self.pets:
            if pet['filename'] == self.current_pet:
                return pet['name']
        return None

    def get_pet_name(self, pet_filename):
        """
        Get the display name for a given pet filename.
        Args:
            pet_filename (str): The pet's filename
        Returns:
            str | None: The pet's display name, or None if not found
        """
        for pet in self.pets:
            if pet['filename'] == pet_filename:
                return pet['name']
        return None

    def is_birthday_today(self):
        """
        Check if today is the user's birthday.
        Returns:
            bool: True if today is the user's birthday, False otherwise
        """
        today = datetime.datetime.now().date()
        return (today.month == self.birthday.month and
                today.day == self.birthday.day)

    def update_login_streak(self, last_login_date):
        """
        Update login streak based on last login date.
        Args:
            last_login_date (datetime.date): The date of the last login
        Returns:
            tuple: (streak_continued, days_since_last_login)
        """
        today = datetime.datetime.now().date()
        days_since_last = (today - last_login_date).days

        if days_since_last == 0:
            # Already logged in today, no change
            return (True, 0)
        elif days_since_last == 1:
            # Logged in yesterday, streak continues
            self.current_login_streak += 1
            if self.current_login_streak > self.longest_login_streak:
                self.longest_login_streak = self.current_login_streak
            return (True, days_since_last)
        else:
            # Streak broken, reset to 1
            self.current_login_streak = 1
            return (False, days_since_last)

    def to_dict(self):
        """Convert user to dictionary for saving"""
        return {
            'username': self.username,
            'birthday': self.birthday.isoformat(),
            'first_login_date': self.first_login_date.isoformat(),
            'last_login_date': self.last_login_date.isoformat(),
            'longest_login_streak': self.longest_login_streak,
            'current_login_streak': self.current_login_streak,
            'pets': self.pets,
            'current_pet': self.current_pet
        }

    @classmethod
    def from_dict(cls, data):
        """Create user from dictionary with validation"""
        # Validate required fields
        required_fields = ['username', 'birthday']
        for field in required_fields:
            if field not in data:
                raise KeyError(f"Missing required field: {field}")

        # Create user
        user = cls(data['username'], data['birthday'])

        # Load pets list (with backward compatibility)
        if 'pets' in data:
            if not isinstance(data['pets'], list):
                raise TypeError("pets must be a list")

            # Handle old format (list of strings) vs new format (list of dicts)
            if data['pets'] and isinstance(data['pets'][0], str):
                # Old format: convert pet names to dict format
                user.pets = [
                    {
                        'name': pet_name,
                        'filename': f"{pet_name.lower().replace(' ', '_')}.json"
                    }
                    for pet_name in data['pets']
                ]
            else:
                # New format: already list of dicts
                user.pets = data['pets']

        # Load current pet (with backward compatibility)
        if 'current_pet' in data:
            current_pet_value = data['current_pet']
            # Check if it's in old format (pet name) or new format (filename)
            if current_pet_value and not current_pet_value.endswith('.json'):
                # Old format: convert pet name to filename
                user.current_pet = f"{current_pet_value.lower().replace(' ', '_')}.json"
            else:
                # New format: already a filename
                user.current_pet = current_pet_value

        # Load login streak data (with backward compatibility)
        if 'first_login_date' in data:
            if isinstance(data['first_login_date'], str):
                user.first_login_date = datetime.date.fromisoformat(data['first_login_date'])
            else:
                user.first_login_date = data['first_login_date']

        if 'last_login_date' in data:
            if isinstance(data['last_login_date'], str):
                user.last_login_date = datetime.date.fromisoformat(data['last_login_date'])
            else:
                user.last_login_date = data['last_login_date']

        if 'longest_login_streak' in data:
            user.longest_login_streak = data['longest_login_streak']

        if 'current_login_streak' in data:
            user.current_login_streak = data['current_login_streak']

        return user

    def __str__(self):
        age = (datetime.datetime.now().date() - self.birthday).days // 365
        pet_count = len(self.pets)
        days_since_first = (datetime.datetime.now().date() - self.first_login_date).days
        current_pet_display = self.get_current_pet_name() or 'None'
        return f"Username: {self.username}\nAge: {age}\nPets owned: {pet_count}\nCurrent pet: {current_pet_display}\nCurrent streak: {self.current_login_streak} days\nLongest streak: {self.longest_login_streak} days\nDays since first login: {days_since_first}"