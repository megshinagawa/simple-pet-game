# Simple Pet Game - Project Structure

This directory contains the core modules for the simple pet game application.

## Module Overview

### Core Modules

#### [pet.py](pet.py)

Defines the `Pet` class representing a virtual pet with needs including fullness and energy.

- Manages pet attributes (name, birthday, age, sleep state)
- Handles stat updates based on time elapsed
- Auto-sleep mechanism when energy reaches 0%
- Feed, sleep, and wake-up actions

#### [user.py](user.py)

Defines the `User` class for managing player profiles.

- User attributes (username, birthday)
- Pet ownership tracking (multiple pets per user)
- Login streak tracking (current and longest streaks)
- Current pet selection management

#### [app_loop.py](app_loop.py)

Contains the main game loop and action handlers.

- Pet initialization and loading logic
- Action handlers (view status, feed, sleep, wake up)
- User settings display
- Game loop orchestration

#### [user_auth.py](user_auth.py)

Handles user authentication and account creation.

- User login/creation flow
- Login streak calculation and messages
- User account selection from existing users

### Supporting Modules

#### [data_handler.py](data_handler.py)

Persistence layer for saving and loading game data.

- Save/load pet data to/from JSON files
- Save/load user data to/from JSON files
- List available users and pets
- File management for the data directory

#### [config.py](config.py)

Central configuration file for game constants.

- File paths for data storage
- Stat boundaries (min/max values)
- Game mechanics rates (sleep restoration, stat decrease)
- Food items and their properties
- Default starting values

### UI Package

#### [ui/](ui/)

Contains UI-related modules for displaying menus and status.

##### [ui/__init__.py](ui/__init__.py)

Exports display functions for easy imports.

##### [ui/menus.py](ui/menus.py)

Display functions for menus and pet status.

- Welcome screen
- Action menu
- Food selection menu
- Pet status display

## Data Storage

### Directory Structure

```txt
data/
├── users/          # User save files (JSON)
│   └── {username}.json
└── pets/           # Pet save files (JSON)
    └── {pet_name}.json
```

### File Formats

**User file structure:**

- Username, birthday, first/last login dates
- Login streak stats
- List of owned pets (with filenames)
- Currently selected pet

**Pet file structure:**

- Pet name, owner, birthday, age
- Current stats (fullness, energy)
- Sleep state and timestamps
- Last update timestamp

## Game Flow

1. **Entry Point**: [../main.py](../main.py)
   - Parses command-line arguments
   - Displays welcome screen

2. **Authentication**: [user_auth.py](user_auth.py)
   - Authenticate or create user
   - Update login streaks

3. **Pet Initialization**: [app_loop.py](app_loop.py) - `initialize_pet()`
   - Load existing pet or create new one
   - Update stats based on time elapsed

4. **Game Loop**: [app_loop.py](app_loop.py) - `run_game_loop()`
   - Display action menu
   - Handle user actions
   - Auto-save on exit

## Key Features

- **Multi-user support**: Each user has their own profile and can own multiple pets
- **Persistent state**: Pets and users are saved as JSON files
- **Time-based mechanics**: Stats decrease over time based on configurable rates
- **Auto-sleep**: Pets automatically sleep when energy reaches 0%
- **Login streaks**: Tracks consecutive daily logins
- **Birthday celebrations**: Special messages on user's birthday
