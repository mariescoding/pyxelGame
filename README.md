# Death Star Escape

Death Star Escape is an engaging maze adventure game developed using Pyxel. The objective of the game is to navigate through the maze, collect all the items (Grogu, Droid1, and Droid2), and avoid the Stormtroopers. The game features unique behaviors for each collectible item, enhancing the gameplay experience.

## Gameplay

- **Objective**: Collect all the items and reach the exit point while avoiding Stormtroopers.
- **Items**:
  - **Grogu**: Grants temporary invincibility to the player.
  - **Droid1**: Reveals a hint or part of the maze.
  - **Droid2**: Slows down all stormtroopers for a limited time.
- **Player Movement**: Use the arrow keys to move the player within the maze. The player cannot move outside the screen dimensions.
- **Stormtroopers**: Move randomly with varying speeds and bounce back upon hitting the screen edges.

## Features

- **Countdown Timer**: The game includes a countdown timer. The game ends automatically when the time runs out.
- **Collision Detection**: Ensures the player can only move within the maze paths and not through walls.
- **Item Collection**: The game checks for item pickups and updates the game state accordingly.

## Tools and Technologies Used

- **Pyxel**: A retro game engine for Python, used to develop the game.
- **Python**: The programming language used to write the game logic.

## Installation and Setup

1. **Install Pyxel**:
    ```sh
    pip install pyxel
    ```

2. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/death-star-escape.git
    cd death-star-escape
    ```

3. **Run the Game**:
    ```sh
    python game.py
    ```

## How to Play

1. **Start the Game**: Press `ENTER` on the title screen to start the game.
2. **Move the Player**: Use the arrow keys (`UP`, `DOWN`, `LEFT`, `RIGHT`) to navigate the maze.
3. **Collect Items**: Click on the items (Grogu, Droid1, Droid2) to collect them and gain their unique benefits.
4. **Avoid Stormtroopers**: Stay away from the stormtroopers to avoid losing lives.
5. **Win Condition**: Collect all items and reach the exit point within the countdown timer to win.
6. **Game Over**: The game will be over if the timer runs out or the player loses all lives.

## Contributions

Contributions are welcome! If you have any ideas for improvements or new features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Pyxel](https://github.com/kitao/pyxel) for providing the game engine used to develop this game.
- All contributors for their suggestions and improvements.

