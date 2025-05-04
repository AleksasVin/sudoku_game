import pygame
from typing import List, Tuple, Optional
from settings import GameSettings, GameTheme

class Cell:
    def __init__(self, value: int, row: int, col: int):
        self._value = value
        self._row = row
        self._col = col
        self._is_initial = value != 0
        self._is_selected = False
        self.settings = GameSettings()

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new_value: int):
        if not self._is_initial:
            self._value = new_value

    @property
    def is_selected(self) -> bool:
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool):
        self._is_selected = value

class DrawableCell(Cell):
    def __init__(self, value: int, row: int, col: int, solution: int):
        super().__init__(value, row, col)
        self._solution = solution
        self._is_hovered = False
        self._is_correct = None  # None means unverified
        self._is_correct_color = GameTheme.INPUT_COLOR  # Default to white
        self._font = pygame.font.Font(None, int(self.settings.CELL_SIZE * 0.7))

    @property
    def is_hovered(self) -> bool:
        return self._is_hovered

    @is_hovered.setter
    def is_hovered(self, value: bool):
        self._is_hovered = value

    def draw(self, screen: pygame.Surface):
        x = self._col * self.settings.CELL_SIZE + self.settings.GRID_OFFSET_X
        y = self._row * self.settings.CELL_SIZE + self.settings.GRID_OFFSET_Y
        cell_rect = pygame.Rect(x, y, self.settings.CELL_SIZE, self.settings.CELL_SIZE)

        # Draw the cell border with selection/highlight if applicable
        if self._is_selected:
            pygame.draw.rect(screen, GameTheme.SELECTED_COLOR, cell_rect)
        elif self._is_hovered:
            pygame.draw.rect(screen, GameTheme.HIGHLIGHT_COLOR, cell_rect)

        # If the cell value is 0 (empty), return early
        if self.value == 0:
            return

        # Center the number inside the cell
        center_x = x + self.settings.CELL_SIZE // 2
        center_y = y + self.settings.CELL_SIZE // 2

        # Draw the number with the color based on its correctness
        text = self._font.render(str(self.value), True, self._is_correct_color)
        text_rect = text.get_rect(center=(center_x, center_y))
        screen.blit(text, text_rect)

    def update_correct_status(self, grid: List[List['DrawableCell']]):
        """
        Updates the correctness of the cell based on its value and solution.
        """
        if self.value == self._solution:
            self._is_correct = True
        else:
            self._is_correct = False

    def is_valid(self, value: int, grid: List[List['DrawableCell']]) -> bool:
        """
        Check if a value is valid in the current row, column, and box.
        """
        # Check the row for duplicates
        for col in range(self.settings.GRID_SIZE):
            if grid[self._row][col].value == value:
                return False

        # Check the column for duplicates
        for row in range(self.settings.GRID_SIZE):
            if grid[row][self._col].value == value:
                return False

        # Check the 3x3 box for duplicates
        start_row = (self._row // 3) * 3
        start_col = (self._col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if grid[r][c].value == value:
                    return False

        return True

    def set_correct_color(self):
        """
        Set the color of the cell based on whether it's correct or not after checking.
        """
        if self._is_correct is True:
            self._is_correct_color = GameTheme.SUCCESS_COLOR  # Green color for correct
        elif self._is_correct is False:
            self._is_correct_color = GameTheme.ERROR_COLOR  # Red color for incorrect
        else:
            self._is_correct_color = GameTheme.INPUT_COLOR  # White color for user input


class Grid:
    def __init__(self, puzzle: List[List[int]], solution: List[List[int]]):
        self.settings = GameSettings()
        self._cells = [
            [DrawableCell(puzzle[row][col], row, col, solution[row][col]) 
            for col in range(self.settings.GRID_SIZE)]
            for row in range(self.settings.GRID_SIZE)
        ]
        self._victory = False
        self.set_initial_correct_colors()

    def set_initial_correct_colors(self):
        for row in self._cells:
            for cell in row:
                if cell.value != 0:
                    cell._is_correct = (cell.value == cell._solution)
                    if cell._is_correct:
                        cell._is_correct_color = GameTheme.SUCCESS_COLOR
                    else:
                        cell._is_correct_color = GameTheme.ERROR_COLOR

    def draw(self, screen: pygame.Surface):
        for row in self._cells:
            for cell in row:
                cell.draw(screen)

        for row in range(self.settings.GRID_SIZE + 1):
            pygame.draw.line(
                screen, GameTheme.GRID_LINE_COLOR,
                (self.settings.GRID_OFFSET_X, self.settings.GRID_OFFSET_Y + row * self.settings.CELL_SIZE),
                (self.settings.GRID_OFFSET_X + self.settings.TOTAL_GRID_SIZE,
                 self.settings.GRID_OFFSET_Y + row * self.settings.CELL_SIZE), 1)

        for col in range(self.settings.GRID_SIZE + 1):
            pygame.draw.line(
                screen, GameTheme.GRID_LINE_COLOR,
                (self.settings.GRID_OFFSET_X + col * self.settings.CELL_SIZE, self.settings.GRID_OFFSET_Y),
                (self.settings.GRID_OFFSET_X + col * self.settings.CELL_SIZE,
                 self.settings.GRID_OFFSET_Y + self.settings.TOTAL_GRID_SIZE), 1)

        for i in range(0, self.settings.GRID_SIZE, 3):
            for j in range(0, self.settings.GRID_SIZE, 3):
                pygame.draw.rect(
                    screen, GameTheme.GRID_LINE_COLOR,
                    pygame.Rect(
                        self.settings.GRID_OFFSET_X + i * self.settings.CELL_SIZE,
                        self.settings.GRID_OFFSET_Y + j * self.settings.CELL_SIZE,
                        3 * self.settings.CELL_SIZE,
                        3 * self.settings.CELL_SIZE
                    ), 3)

    def select_cell(self, row: int, col: int):
        for r in range(self.settings.GRID_SIZE):
            for c in range(self.settings.GRID_SIZE):
                self._cells[r][c].is_selected = False
        self._cells[row][col].is_selected = True

    def set_value(self, value: int):
        for row in self._cells:
            for cell in row:
                if cell.is_selected:
                    cell.value = value
                    cell.update_correct_status(self._cells)
                    cell._is_correct = None
                    if self._check_victory():
                        self._victory = True
                    return

    def handle_hover(self, mouse_pos: Tuple[int, int]):
        x, y = mouse_pos
        adjusted_x = x - self.settings.GRID_OFFSET_X
        adjusted_y = y - self.settings.GRID_OFFSET_Y
        row = adjusted_y // self.settings.CELL_SIZE
        col = adjusted_x // self.settings.CELL_SIZE

        if 0 <= row < self.settings.GRID_SIZE and 0 <= col < self.settings.GRID_SIZE:
            for r in range(self.settings.GRID_SIZE):
                for c in range(self.settings.GRID_SIZE):
                    self._cells[r][c].is_hovered = False
            self._cells[row][col].is_hovered = True

    def _check_victory(self):
        for row in range(self.settings.GRID_SIZE):
            for col in range(self.settings.GRID_SIZE):
                if self._cells[row][col].value != self._cells[row][col]._solution:
                    return False
        return True

    @property
    def victory(self):
        return self._victory
