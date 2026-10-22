# 🐍 Snake Game

A classic Snake game built with **Python and Pygame**, featuring screen wraparound, food collection, score tracking, and a persistent SQLite leaderboard.

Control the snake, collect food, increase your score, and try to beat your personal best!

## 🎮 Features

- **Classic Snake Gameplay** — Control the snake and collect food to increase your score.
- **Wall Wraparound** — Pass through any screen boundary and reappear on the opposite side.
- **Self-Collision Detection** — The game ends when the snake runs into its own body.
- **Dynamic Difficulty** — The snake's speed increases as your score grows.
- **Persistent Leaderboard** — Scores are stored in an SQLite database and remain available between sessions.
- **Restart Support** — Start a new game without restarting the application.

## 🖥️ Preview


## 🛠️ Built With

| Technology | Purpose |
|---|---|
| Python | Core game logic |
| Pygame | Game window, graphics, keyboard input, and game loop |
| SQLite | Persistent score storage |

## 📋 Requirements

- Python 3
- Pygame

SQLite is included with Python through the `sqlite3` module, so no separate database installation is required.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/snake-game.git
cd snake-game
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install Pygame

Using pip:

```bash
python -m pip install pygame
```

On NixOS, you can run the game with a temporary environment:

```bash
nix-shell -p python3 python3Packages.pygame --run "python main.py"
```

### 3. Run the game

```bash
python main.py
```

Enter your player name when prompted, then start playing.

## 🕹️ Controls

| Key | Action |
|---|---|
| `↑` | Move up |
| `↓` | Move down |
| `←` | Move left |
| `→` | Move right |
| `R` | Restart after game over |
| `L` | View the leaderboard |
| `Q` | Quit from the game-over or leaderboard screen |

## 🧩 How to Play

1. Control the snake using the arrow keys.
2. Eat the red food to earn **10 points**.
3. Each time you collect food, the snake grows.
4. The snake moves faster as your score increases.
5. Avoid running into your own body.
6. Use the screen boundaries to wrap around to the opposite side.
7. Try to achieve the highest score possible!

## 💾 Leaderboard

The game uses SQLite to save player scores locally.

- Database file: `snake_game.db`
- Table: `scores`
- Stored information: player name and score
- Leaderboard: Displays the top five scores in descending order

The database is automatically created when the game starts. You do not need to configure it manually.

## 📁 Project Structure

```text
snake-game/
├── main.py          # Game logic and entry point
├── snake_game.db    # SQLite database (created automatically)
├── README.md         # Project documentation
└── .gitignore       # Files excluded from Git
```

The database file is generated when you run the game for the first time. It does not need to be committed to GitHub.

## 🧠 What I Learned

This project explores practical Python programming concepts, including:

- Game loops and event handling with Pygame
- 2D grid-based movement and coordinate calculations
- Collision detection and boundary wraparound
- Functions and state management
- Random food generation
- SQLite database operations
- Persistent data storage
- Keyboard input and real-time graphics

## 🔮 Possible Improvements

Ideas for future development:

- Pause and resume functionality
- Difficulty selection
- High-score highlighting
- Sound effects and background music
- A graphical player-name input screen
- Improved game-over and menu screens
- Unit tests for movement, collision, and database logic

## 📜 License

This project is open source. You may use, modify, and distribute it under the terms of the [MIT License](LICENSE), provided you add an MIT `LICENSE` file to the repository.

---

**Built with Python and Pygame.**
