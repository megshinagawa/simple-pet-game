SAVE_FILENAME = 'data/pet_data.json'

# Stat boundaries
MIN_STAT = 0.0
MAX_STAT = 100.0

# Sleep mechanics
SLEEP_RESTORATION_RATE = 288  # seconds per 1 energy point (8 hours = full restore)
SLEEP_FULLNESS_MULTIPLIER = 0.3  # Fullness decreases at 30% rate while sleeping

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
