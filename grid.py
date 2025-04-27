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
        self._is_correct = True if value != 0 else None
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

        if self._is_selected:
            pygame.draw.rect(screen, GameTheme.SELECTED_COLOR, cell_rect)
        elif self._is_hovered:
            pygame.draw.rect(screen, GameTheme.HIGHLIGHT_COLOR, cell_rect)

        if self.value == 0:
            return

        center_x = x + self.settings.CELL_SIZE // 2
        center_y = y + self.settings.CELL_SIZE // 2

        if self._is_correct is False:
            color = GameTheme.ERROR_COLOR
        elif self._is_correct is True:
            color = GameTheme.SUCCESS_COLOR
        else:
            color = GameTheme.INPUT_COLOR

        text = self._font.render(str(self.value), True, color)
        text_rect = text.get_rect(center=(center_x, center_y))
        screen.blit(text, text_rect)

    def update_correct_status(self, grid: List[List['DrawableCell']]):
        if self.value == self._solution:
            self._is_correct = True
        else:
            self._is_correct = False

class Grid:
    def __init__(self, puzzle: List[List[int]], solution: List[List[int]]):
        self.settings = GameSettings()
        self._cells = [
            [DrawableCell(puzzle[row][col], row, col, solution[row][col]) 
            for col in range(self.settings.GRID_SIZE)]
            for row in range(self.settings.GRID_SIZE)
        ]
        self._victory = False

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