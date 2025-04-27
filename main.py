import pygame
from settings import GameSettings
from ui.menu import DifficultyMenu
from grid import Grid
from puzzle import PuzzleGenerator
from ui.controls import GameControls
from ui.victory import VictoryScreen

class SudokuGame:
    def __init__(self):
        pygame.init()
        self.settings = GameSettings()
        self.screen = pygame.display.set_mode(
            (self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku")
        
        self.menu = DifficultyMenu()
        self.game_started = False
        self.grid = None
        self.puzzle = None
        self.solution = None
        self.victory_screen = None
        self.game_controls = GameControls()

    def start_game(self, difficulty_config: dict):
        self.settings.update_grid_size(difficulty_config['grid_size'])
        generator = PuzzleGenerator()
        self.puzzle, self.solution = generator.generate_puzzle(difficulty_config)
        self.grid = Grid(self.puzzle, self.solution)
        self.game_started = True
        self.victory_screen = None

    def handle_event(self, event):
        if not self.game_started:
            difficulty_config = self.menu.handle_event(event)
            if difficulty_config is not None:
                self.start_game(difficulty_config)
                return None
            return None
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                control_action = self.game_controls.handle_event(event)

                if control_action == 'menu':
                    self.game_started = False
                    self.menu = DifficultyMenu()
                    self.victory_screen = None
                    return None
                elif control_action == 'exit':
                    pygame.quit()
                    return 'exit'

                if self.grid._victory and self.victory_screen:
                    if self.victory_screen.check_restart_click(pos):
                        self.game_started = False
                        self.victory_screen = None
                        self.menu = DifficultyMenu()
                        return None

                if control_action == 'check':
                    self.check_numbers()
                    return None

                if control_action == 'clear':
                    self.clear_board()
                    return None

                adjusted_x = pos[0] - self.settings.GRID_OFFSET_X
                adjusted_y = pos[1] - self.settings.GRID_OFFSET_Y
                row = adjusted_y // self.settings.CELL_SIZE
                col = adjusted_x // self.settings.CELL_SIZE
                if (0 <= row < 9 and 0 <= col < 9):
                    self.grid.select_cell(row, col)
                    return None
                return None

            elif event.type == pygame.MOUSEMOTION:
                self.grid.handle_hover(pygame.mouse.get_pos())
                self.game_controls.handle_event(event)
                return None

            elif event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    self.grid.set_value(int(event.unicode))
                    return None
                return None
            return None

    def check_numbers(self):
        for row in self.grid._cells:
            for cell in row:
                if cell._is_correct is None and cell.value != 0:
                    cell._is_correct = (cell.value == cell._solution)

    def clear_board(self):
        for row in self.grid._cells:
            for cell in row:
                if not cell._is_initial:
                    cell.value = 0
                    cell._is_correct = None

    def draw(self):
        if not self.game_started:
            self.menu.draw(self.screen)
        else:
            self.screen.fill(self.settings.BACKGROUND_COLOR)
            self.grid.draw(self.screen)
            self.game_controls.draw(self.screen)

            if self.grid._victory:
                if self.victory_screen is None:
                    self.victory_screen = VictoryScreen(self.puzzle, self.solution)
                self.victory_screen.draw(self.screen)

            pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                result = self.handle_event(event)
                if result == 'exit':
                    running = False

            try:
                self.draw()
                pygame.display.flip()
            except pygame.error:
                running = False

        pygame.quit()

if __name__ == "__main__":
    game = SudokuGame()
    game.run()