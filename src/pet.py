import datetime
from src.config import (
    MIN_STAT,
    MAX_STAT,
    SLEEP_RESTORATION_RATE,
    SLEEP_FULLNESS_MULTIPLIER,
    FULLNESS_DECREASE_RATE,
    ENERGY_DECREASE_RATE,
    DEFAULT_FULLNESS,
    DEFAULT_ENERGY
)


class Pet:
    """
    A virtual pet that can be fed, put to sleep, and cared for.

    This class represents a pet with basic needs including fullness and energy.
    The pet has a birthday, ages over time, and requires feeding and sleep
    to maintain its stats. Fullness decreases and energy decreases over time.

    Attributes:
        name (str): The pet's name
        birthday (datetime.date): The date the pet was created
        age (int): The pet's age in days
        sleep (bool): Whether the pet is currently sleeping
        sleep_start (datetime.datetime | None): When the pet started sleeping
        last_update (datetime.datetime): When stats were last updated
        fullness (int): Fullness level from 0 (starving) to 100 (full)
        energy (int): Energy level from 0 (exhausted) to 100 (fully energized)
    """

    def __init__(self, name):
        """
        Initializes Pet instance
        Args:
            name (str): pet name
        """
        if not isinstance(name, str):
            raise TypeError("Pet name must be a string")
        if not name or not name.strip():
            raise ValueError("Pet name cannot be empty")
        if len(name) > 50:
            raise ValueError("Pet name cannot exceed 50 characters")
        self.name = name.strip()

        # life info
        self.birthday = datetime.datetime.now().date()
        self.age = 0

        # sleep
        self.sleep = False
        self.sleep_start = None

        # stats
        self.last_update = datetime.datetime.now()
        self.fullness = DEFAULT_FULLNESS
        self.energy = DEFAULT_ENERGY

        # tracking time at zero stats
        self.fullness_zero_since = None  # timestamp when fullness first hit 0
        self.energy_zero_since = None  # timestamp when energy first hit 0


    def update_stats(self):
        """
        Update fullness and energy based on elapsed time.
        Fullness decreases over time (slower while sleeping).
        Energy decreases over time (but not while sleeping).
        """
        now = datetime.datetime.now()
        elapsed_seconds = (now - self.last_update).total_seconds()

        # Store old values to calculate when stats hit zero
        old_fullness = self.fullness
        old_energy = self.energy

        # Calculate fullness decrease (slower when sleeping)
        fullness_multiplier = SLEEP_FULLNESS_MULTIPLIER if self.sleep else 1.0
        fullness_change = (elapsed_seconds / FULLNESS_DECREASE_RATE) * fullness_multiplier
        self.fullness -= fullness_change

        # Only decrease energy if pet is not sleeping
        if not self.sleep:
            energy_change = elapsed_seconds / ENERGY_DECREASE_RATE
            self.energy -= energy_change

        # Calculate when fullness hit zero (if it did)
        if old_fullness > MIN_STAT and self.fullness <= MIN_STAT:
            # Calculate how long ago fullness hit zero
            fullness_rate = 1.0 / (FULLNESS_DECREASE_RATE * fullness_multiplier)  # points per second
            seconds_to_zero = old_fullness / fullness_rate
            self.fullness_zero_since = self.last_update + datetime.timedelta(seconds=seconds_to_zero)
        elif self.fullness > MIN_STAT:
            self.fullness_zero_since = None

        # Calculate when energy hit zero (if it did)
        if not self.sleep and old_energy > MIN_STAT and self.energy <= MIN_STAT:
            # Calculate how long ago energy hit zero
            energy_rate = 1.0 / ENERGY_DECREASE_RATE  # points per second
            seconds_to_zero = old_energy / energy_rate
            self.energy_zero_since = self.last_update + datetime.timedelta(seconds=seconds_to_zero)
        elif self.energy > MIN_STAT:
            self.energy_zero_since = None

        # Cap the stat values
        self.fullness = max(MIN_STAT, min(MAX_STAT, self.fullness))
        self.energy = max(MIN_STAT, min(MAX_STAT, self.energy))

        # Update the last_update timestamp
        self.last_update = now

        # Update age
        self.age = (datetime.datetime.now().date() - self.birthday).days


    def go_to_bed(self):
        """
        Put your pet to sleep
        Return:
            bool: success status of sleeping
        """
        # Set sleep properties
        self.sleep = True
        self.sleep_start = datetime.datetime.now()
        return True
    

    def wake_up(self):
        """
        Wake your pet up from sleep
        Return:
            bool: success status of waking up
        """
        # Update energy stat
        if self.sleep_start is not None:
            seconds_slept = (datetime.datetime.now() - self.sleep_start).total_seconds()
            energy_restored = seconds_slept / SLEEP_RESTORATION_RATE
            self.energy += energy_restored

            # Cap the stat value
            self.energy = max(MIN_STAT, min(MAX_STAT, self.energy))

            # Reset zero stat timer if energy is now above zero
            if self.energy > MIN_STAT:
                self.energy_zero_since = None

        # Clear sleep properties
        self.sleep = False
        self.sleep_start = None

        # Return success status
        return True
    
    
    def feed(self, fill_value):
        """
        Feed pet food
        Args:
            fill_value (int): amount of fullness to increase (positive)
        Return:
            bool: success status of feeding
        """
        # Validate fill_value parameter
        if not isinstance(fill_value, (int, float)):
            raise TypeError("fill_value must be a number")
        if fill_value <= 0:
            raise ValueError("fill_value must be positive")
        if fill_value > 100:
            raise ValueError("fill_value cannot exceed 100")

        # Update fullness meter
        self.fullness += fill_value

        # Cap the stat value
        self.fullness = max(MIN_STAT, min(MAX_STAT, self.fullness))

        # Reset zero stat timer if fullness is now above zero
        if self.fullness > MIN_STAT:
            self.fullness_zero_since = None

        # Return success status True
        return True
    

    def to_dict(self):
        """Convert pet to dictionary for saving"""
        return {
            'name': self.name,
            'birthday': self.birthday.isoformat(),
            'age': self.age,
            'sleep': self.sleep,
            'sleep_start': self.sleep_start.isoformat() if self.sleep_start else None,
            'last_update': self.last_update.isoformat(),
            'fullness': self.fullness,
            'energy': self.energy,
            'fullness_zero_since': self.fullness_zero_since.isoformat() if self.fullness_zero_since else None,
            'energy_zero_since': self.energy_zero_since.isoformat() if self.energy_zero_since else None
        }


    def __str__(self):
        result = f"Name: {self.name}\nAge: {self.age}\nFullness: {int(self.fullness)}%\nEnergy: {int(self.energy)}%\nStatus: {'Sleeping' if self.sleep else 'Awake'}"

        # Add time at 0% for fullness
        if self.fullness_zero_since is not None:
            duration = datetime.datetime.now() - self.fullness_zero_since
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            seconds = int(duration.total_seconds() % 60)

            if hours > 0:
                result += f"\nFullness at 0% for: {hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                result += f"\nFullness at 0% for: {minutes}m {seconds}s"
            else:
                result += f"\nFullness at 0% for: {seconds}s"

        # Add time at 0% for energy
        if self.energy_zero_since is not None:
            duration = datetime.datetime.now() - self.energy_zero_since
            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)
            seconds = int(duration.total_seconds() % 60)

            if hours > 0:
                result += f"\nEnergy at 0% for: {hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                result += f"\nEnergy at 0% for: {minutes}m {seconds}s"
            else:
                result += f"\nEnergy at 0% for: {seconds}s"

        return result


    @classmethod
    def from_dict(cls, data):
        """Create pet from dictionary with validation"""
        # Validate required fields exist (support both old 'hunger' and new 'fullness' format)
        required_fields = ['name', 'birthday', 'age', 'sleep', 'energy']
        for field in required_fields:
            if field not in data:
                raise KeyError(f"Missing required field: {field}")

        # Check for either fullness or hunger (backward compatibility)
        if 'fullness' not in data and 'hunger' not in data:
            raise KeyError("Missing required field: 'fullness' (or legacy 'hunger')")

        # Validate and create pet (name validation happens in __init__)
        pet = cls(data['name'])

        # Validate and set birthday
        if not isinstance(data['birthday'], str):
            raise TypeError("birthday must be a string")
        try:
            pet.birthday = datetime.date.fromisoformat(data['birthday'])
        except ValueError as e:
            raise ValueError(f"Invalid birthday format: {e}")

        # Validate age
        if not isinstance(data['age'], int):
            raise TypeError("age must be an integer")
        if data['age'] < 0:
            raise ValueError("age cannot be negative")
        pet.age = data['age']

        # Validate sleep state
        if not isinstance(data['sleep'], bool):
            raise TypeError("sleep must be a boolean")
        pet.sleep = data['sleep']

        # Validate sleep_start
        if 'sleep_start' in data and data['sleep_start'] is not None:
            if not isinstance(data['sleep_start'], str):
                raise TypeError("sleep_start must be a string or None")
            try:
                pet.sleep_start = datetime.datetime.fromisoformat(data['sleep_start'])
            except ValueError as e:
                raise ValueError(f"Invalid sleep_start format: {e}")
        else:
            pet.sleep_start = None

        # Validate last_update
        last_update_str = data.get('last_update', datetime.datetime.now().isoformat())
        if not isinstance(last_update_str, str):
            raise TypeError("last_update must be a string")
        try:
            pet.last_update = datetime.datetime.fromisoformat(last_update_str)
        except ValueError as e:
            raise ValueError(f"Invalid last_update format: {e}")

        # Validate fullness (with backward compatibility for 'hunger')
        if 'fullness' in data:
            fullness_value = data['fullness']
        else:
            # Convert old 'hunger' format to 'fullness' (hunger was inverted: 0=full, 100=starving)
            fullness_value = MAX_STAT - data['hunger']

        if not isinstance(fullness_value, (int, float)):
            raise TypeError("fullness must be a number")
        if not MIN_STAT <= fullness_value <= MAX_STAT:
            raise ValueError(f"fullness must be between {MIN_STAT} and {MAX_STAT}")
        pet.fullness = fullness_value

        # Validate energy
        if not isinstance(data['energy'], (int, float)):
            raise TypeError("energy must be a number")
        if not MIN_STAT <= data['energy'] <= MAX_STAT:
            raise ValueError(f"energy must be between {MIN_STAT} and {MAX_STAT}")
        pet.energy = data['energy']

        # Load zero stat tracking fields (optional for backward compatibility)
        if 'fullness_zero_since' in data and data['fullness_zero_since'] is not None:
            if not isinstance(data['fullness_zero_since'], str):
                raise TypeError("fullness_zero_since must be a string or None")
            try:
                pet.fullness_zero_since = datetime.datetime.fromisoformat(data['fullness_zero_since'])
            except ValueError as e:
                raise ValueError(f"Invalid fullness_zero_since format: {e}")
        else:
            pet.fullness_zero_since = None

        if 'energy_zero_since' in data and data['energy_zero_since'] is not None:
            if not isinstance(data['energy_zero_since'], str):
                raise TypeError("energy_zero_since must be a string or None")
            try:
                pet.energy_zero_since = datetime.datetime.fromisoformat(data['energy_zero_since'])
            except ValueError as e:
                raise ValueError(f"Invalid energy_zero_since format: {e}")
        else:
            pet.energy_zero_since = None

        return pet