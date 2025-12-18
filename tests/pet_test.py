import time
import sys
from pathlib import Path

# Add parent directory to path so we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pet import Pet


def main():
    """Test function for Pet class"""
    print("=== Pet Game Test ===\n")

    # Create a new pet
    my_pet = Pet("Fluffy")
    print(f"Created pet: {my_pet.name}")
    print(f"Birthday: {my_pet.birthday}")
    print(f"Age: {my_pet.age} days")
    print(f"Initial hunger: {my_pet.hunger}")
    print(f"Initial energy: {my_pet.energy}\n")

    # Test feeding
    print("--- Testing Feed ---")
    print(f"Feeding {my_pet.name} 20 points...")
    my_pet.feed(20)
    print(f"Hunger after feeding: {my_pet.hunger}\n")

    # Test feeding when full
    print("Feeding until full...")
    my_pet.feed(100)
    print(f"Hunger after max feeding: {my_pet.hunger}")
    my_pet.feed(10)  # Should print "already full" message
    print()

    # Test sleep
    print("--- Testing Sleep ---")
    print(f"Putting {my_pet.name} to sleep...")
    my_pet.go_to_bed()
    print(f"Is sleeping: {my_pet.sleep}")

    # Try to sleep again (should fail)
    my_pet.go_to_bed()
    print()

    # Wait a bit then wake up
    print("Waiting 30 seconds...")
    time.sleep(30)

    print(f"Waking up {my_pet.name}...")
    my_pet.wake_up()
    print(f"Energy after 30 seconds of sleep: {my_pet.energy}")
    print(f"Is sleeping: {my_pet.sleep}\n")

    # Test age update
    print("--- Testing Age Update ---")
    my_pet.update_age()
    print(f"Current age: {my_pet.age} days")


if __name__ == "__main__":
    main()
