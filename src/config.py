import os

DATA_PATH = "data"
USERS_PATH = os.path.join(DATA_PATH, "users")
PETS_PATH = os.path.join(DATA_PATH, "pets")

PET_DATA_DEFAULT_FILE = 'pet.json'
USER_DATA_DEFAULT_FILE = 'user.json'

# Construct full save paths
PET_DATA_PATH = os.path.join(PETS_PATH, PET_DATA_DEFAULT_FILE)
USER_DATA_PATH = os.path.join(USERS_PATH, USER_DATA_DEFAULT_FILE)

# Stat boundaries
MIN_STAT = 0.0
MAX_STAT = 100.0

# Sleep mechanics
SLEEP_RESTORATION_RATE = 288  # seconds per 1 energy point (8 hours = full restore)
SLEEP_FULLNESS_MULTIPLIER = 0.1  # Fullness decreases at 10% rate while sleeping

# Passive stat changes over time
FULLNESS_DECREASE_RATE = 216  # seconds per 1 fullness point (6 hours = fully hungry)
ENERGY_DECREASE_RATE = 576  # seconds per 1 energy point (16 hours = fully exhausted)

# Default starting values
DEFAULT_FULLNESS = 20.0  # Pet starts somewhat hungry
DEFAULT_ENERGY = 20.0  # Pet starts with low energy

# Food items (id, name, fill_value)
FOODS = {
    1: {"name": "Rice ball", "fill_value": 20},
    2: {"name": "Tomato", "fill_value": 15},
    3: {"name": "Candy", "fill_value": 5}
}
