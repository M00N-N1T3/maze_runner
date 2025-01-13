# Robot

**Robot** is an interactive maze-solving game written in Python. It leverages the `turtle` and `tkinter` libraries to provide both Command-Line Interface (CLI) and Graphical User Interface (GUI) modes.

## Features

- Two gameplay modes:
  - **CLI Mode**: Default mode for a simplified experience.
  - **GUI Mode**: Uses `turtle` for a visual representation of the maze and the robot's traversal.
- Two maze options:
  - **Simple Maze**: A straightforward maze for beginners.
  - **Garden of Eden**: A more complex and challenging maze.
- Maze-solving functionality with customizable traversal directions.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/M00N-N1T3/maze_runner.git
cd maze_runner
```

Ensure you have Python installed (version 3.6 or newer). You will also need the following Python libraries:

- `turtle`
- `tkinter`

These libraries typically come pre-installed with Python on most systems.

## Usage

### Running the Game

The game can be executed in two modes: CLI (default) and GUI (requires additional argument).

#### CLI Mode (Default)

To run the game in CLI mode:

```bash
python robot.py [maze_name]
```

- **`maze_name`**: The name of the maze to load (default is `simple`).

#### GUI Mode

To enable GUI mode, pass `turtle` as the second argument:

```bash
python robot.py [maze_name] turtle
```

- **`maze_name`**: The name of the maze to load (default is `simple`).
- **`turtle`**: Enables the graphical interface.

### Solving the Maze Automatically

The game includes an automatic maze-solving feature. Use the mazerun command to activate it:

```bash
mazerun [north] [south] [west] [east]
```

- **`north`**: The starting direction (default direction).
- **`south`**, **`west`**, **`east`**: Optional arguments for configuring traversal directions.

## Examples

1. Run the game in CLI mode with the default maze:

   ```bash
   python robot.py
   ```

2. Run the game in GUI mode with the `Garden of Eden` maze:

   ```bash
   python robot.py garden_of_eden turtle
   ```

3. Solve the maze automatically starting from the north:

   ```bash
   mazerun north south west east
   ```

## Acknowledgments

- The `turtle` library for providing a simple yet powerful way to create GUIs.
- The `tkinter` library for additional GUI components

