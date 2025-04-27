# Sudoku Game 

## Introduction

### What is this application?

This is a Python-based Sudoku game featuring:

- Three difficulty levels: **Easy**, **Medium**, **Hard**
- Ability to load custom Sudoku boards
- Interactive GUI built using **Pygame**
- Input validation and victory detection
- Solution saving functionality

### How to run the program?

1. **Clone the repository**:

    ```bash
    git clone https://github.com/AleksasVin/sudoku_game
    ```

2. **Install dependencies**:

    ```bash
    pip install pygame numpy
    ```

3. **Run the game**:

    ```bash
    python main.py
    ```

### How to use the program?

- **Select difficulty**: Choose from the menu options (Easy, Medium, Hard)
- **Click cells** to select them
- **Press number keys (1-9)** to fill cells
- **Use buttons**:
  - **Menu**: Return to the main menu
  - **Exit**: Quit the game
  - **Check**: Validate the current inputs
  - **Clear**: Reset all user inputs
- For **custom boards**:
  - Create a `custom_sudoku_board.txt` file with your puzzle.
  - Select the "Load Custom Board" option.

## Design and Implementation

### Functional Requirements Implementation

#### 1. Object-Oriented Programming (OOP) Principles

- **Encapsulation**:  
  Classes encapsulate internal state to protect data integrity.

    ```python
    class Cell:
        def __init__(self, value: int, row: int, col: int):
            self._value = value  # Protected attribute
            self._row = row
            self._col = col
            
        @property
        def value(self) -> int:  # Controlled access
            return self._value
    ```

- **Abstraction**:  
  The `PuzzleGenerator` class hides the complexity of puzzle generation.

    ```python
    class PuzzleGenerator:
        def generate_puzzle(self, difficulty_config: dict):
            """Simple interface hiding implementation"""
            solution = self._generate_complete_solution()
            puzzle = self._remove_numbers(solution, difficulty_config)
            return puzzle, solution
    ```

- **Inheritance**:  
  `DrawableCell` extends the `Cell` class to add drawing functionality.

    ```python
    class DrawableCell(Cell):
        def __init__(self, value: int, row: int, col: int, solution: int):
            super().__init__(value, row, col)
            self._solution = solution
    ```

- **Polymorphism**:  
  UI elements (e.g., menu, grid) share a common interface.

    ```python
    def draw(self, screen: pygame.Surface):
        """Implemented differently by Menu, Grid, etc."""
        raise NotImplementedError
    ```

#### 2. Design Patterns

- **Factory Method**:  
  Used in the `DifficultyMenu` to create different game configurations.

    ```python
    def handle_event(self, event):
        if difficulty == 'Load Custom Board':
            return self._create_custom_config()  # Factory method
        return self.settings.DIFFICULTY_CONFIGS[difficulty]  # Predefined configs
    ```

- **Composition/Aggregation**:  
  The `SudokuGame` class is composed of multiple components (e.g., menu, controls, grid).

    ```python
    class SudokuGame:
        def __init__(self):
            self.menu = DifficultyMenu()  # Composition
            self.grid = None  # Aggregation
            self.game_controls = GameControls()  # Composition
    ```

### File Operations

- **Custom Board Loading**:

    ```python
    with open('custom_sudoku_board.txt', 'r') as f:
        puzzle = [[int(num) for num in line.split()] for line in f]
    ```

- **Solution Saving**:

    ```python
    with open('custom_sudoku_board_solved.txt', 'w') as f:
        for row in solution:
            f.write(' '.join(map(str, row)) + '\n')
    ```

### Testing

- Unit tests cover core functionality, such as victory detection.

    ```python
    class TestGrid(unittest.TestCase):
        def test_victory_condition(self):
            grid = create_test_grid()
            grid.set_value(3)  # Correct value
            self.assertTrue(grid.victory)
    ```

## Results and Summary

### Results

- Fully playable Sudoku game with GUI
- Valid move checking and victory detection
- Successful implementation of:
  - OOP principles (Encapsulation, Abstraction, Inheritance, Polymorphism)
  - Factory Method design pattern
  - File I/O operations (loading and saving puzzles)
  - Unit testing

### Conclusions

The project successfully demonstrates:
- Clean OOP architecture
- Effective use of design patterns
- Proper separation of concerns
- Robust error handling

### Future Extensions

- **Database Integration**: Store puzzles and track high scores.
- **Hint System**: Provide assistance for solving puzzles.
- **Multiplayer Mode**: Add competitive gameplay.
- **Advanced Analytics**: Track player statistics and puzzle-solving metrics.

## Resources

- https://www.geeksforgeeks.org/building-and-visualizing-sudoku-game-using-pygame/

### Code Style

- Follows [PEP 8 guidelines](https://pep8.org/) with:
  - Descriptive variable names
  - Consistent indentation
  - Type hints
  - Docstrings for major functions
  - 79-character line limits

The complete implementation demonstrates solid software engineering principles while delivering an engaging Sudoku gaming experience.
