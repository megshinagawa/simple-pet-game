# Simple Pet Game

A command-line virtual pet game where you care for your pet by feeding it and managing its sleep schedule. Watch your pet age over time while keeping it happy and healthy.

## Features

- **Virtual Pet Care**: Feed your pet and manage its sleep to keep it healthy
- **Real-time Stats**: Pet's fullness and energy levels decrease over time, even when you're not playing
- **Persistent Save System**: Your pet's state is automatically saved and ages even between play sessions
- **Multiple Food Options**: Choose from different foods with varying fullness values
- **Sleep Mechanics**: Put your pet to sleep to restore energy (fullness decreases slower while sleeping)

## Game Mechanics

### Stats

- **Fullness**: Decreases over time. When sleeping, decreases slower.
- **Energy**: Decreases over time when awake. Restores while sleeping.
- **Age**: Your pet ages in real-time based on days since birth.

### Actions

1. **View Pet Status**: Check your pet's current stats and age
2. **Feed Pet**: Choose from available foods to restore fullness
3. **Go to Bed**: Put your pet to sleep (restores energy but can't eat while sleeping)
4. **Wake Up**: Wake your pet from sleep
5. **Save and Exit**: Save your progress and quit the game

### Food Options

- **Rice ball**: +20 fullness
- **Tomato**: +15 fullness
- **Candy**: +5 fullness

## Installation

### Requirements

- Python 3.7 or higher
