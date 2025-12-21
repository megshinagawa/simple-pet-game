import random
from src.config import TOTAL_GAME_COUNT, DIRECTIONS

def play_which_way(pet):
    """
    Your game description.
    
    Args:
        pet (Pet): The current pet
    
    Returns:
        bool: True if game completed successfully
    """
    while True:
        game_instructions = input("Do you want to read the game instruction? (y/n) ").strip()
        if game_instructions == 'y':
            print("GAME INSTRUCTIONS")
            break
        elif game_instructions == 'n':
            print("Continuing to game...")
            break
        else:
            print("Invalid answer. Please enter 'y' or 'n'")

    game_count = 0
    correct_count = 0

    while game_count < TOTAL_GAME_COUNT:
        game_count += 1
        print("-" * 50)
        print(f"Game: {game_count}/{TOTAL_GAME_COUNT}")
        correct = random.choice(list(DIRECTIONS.keys()))

        while True:
            user_answer = input(f"Which way did {pet.name} go? (l/r) ").strip()
            if user_answer in DIRECTIONS:
                break
            else:
                print("Invalid answer. Please enter a valid direction.")

        print(f"You look {DIRECTIONS[user_answer]}...")
        
        if correct == user_answer:
            print(f"{pet.name}: Boo! You found me!")
            print(f">> Hooray! You found {pet.name}!")
            
            correct_count += 1
        else:
            print(f"{pet.name}: The correct answer was '{DIRECTIONS[correct]}'!")
            print(">> Better luck next time!")
    
    print("-" * 50)
    print(f"{pet.name}: You won {correct_count} times, which means...")

    if correct_count > (TOTAL_GAME_COUNT // 2):
        print(f"{pet.name}: YOU WIN!")
        return True
    else:
        print(f"{pet.name}: I WIN!")
        return False