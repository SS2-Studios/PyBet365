# PyBet365

**PyBet365** is a Python-based game that simulates horse racing, allowing players to bet on different horses and participate in exciting races.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SS2-Studios/PyBet365.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd PyBet365
   ```

3. **Install required libraries:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

Run the main file `main.py` to start the game:
```bash
python main.py
```

## Project Structure

The project consists of the following files:

- **`main.py`**: The main file to launch the game.

- **`game.py`**: Contains the core game logic, including race creation and game flow management.

- **`assets.py`**: Defines resources such as images and sounds used in the game.

- **`config.py`**: Includes game configuration parameters, such as horse speed and race duration.

- **`utils.py`**: Helper functions that support the main game logic.

- **`track_background.jpg`**: An image representing the race track background.

- **`horse.png`**: The image of a horse participating in the race.

- **`start_race.wav`**: A sound played at the start of the race.

- **`horse_running.wav`**: The sound of horses running during the race.

- **`win_sound.wav`**: A sound played when the player wins.

- **`lose_sound.wav`**: A sound played when the player loses.

## How to Play

1. **Launch the Game:** Upon running `main.py`, the game will load and display the main menu.

2. **Place Bets:** Players can choose a horse to bet on and enter the amount of the bet.

3. **Start the Race:** Once the bet is placed, the race begins.

4. **Results:** After the race, the game displays whether the player won or lost based on the race outcome.

## Requirements

- Python 3.x
- Pygame library

## Notes

- The game is intended for entertainment purposes and does not involve real betting.
- All audio and graphical assets are included in the project.

Enjoy the game!
