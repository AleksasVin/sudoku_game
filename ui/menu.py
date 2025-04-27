import pygame
from typing import Optional
from settings import GameSettings

class DifficultyMenu:
    def __init__(self):
        self.settings = GameSettings()
        self._font = pygame.font.Font(None, 36)
        self._title_font = pygame.font.Font(pygame.font.get_default_font(), 80)
        
        self.button_width = 250
        self.button_height = 60
        self.button_margin = 30
        
        start_y = self.settings.WINDOW_HEIGHT // 2 - 90
        self.buttons = {}
        
        difficulties = ['Easy', 'Medium', 'Hard', 'Load Custom Board']
        for i, difficulty in enumerate(difficulties):
            button_x = self.settings.WINDOW_WIDTH // 2 - self.button_width // 2
            button_y = start_y + i * (self.button_height + self.button_margin)
            self.buttons[difficulty] = pygame.Rect(button_x, button_y,
                                                self.button_width, self.button_height)

        self.button_color = (40, 60, 100)
        self.hover_color = (60, 80, 120)
        self.text_color = (255, 255, 255)
        self.title_color = (0, 200, 255)
        self._hovered_button = None

    def handle_event(self, event) -> Optional[dict]:
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self._hovered_button = None
            for difficulty, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    self._hovered_button = difficulty
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for difficulty, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    if difficulty == 'Load Custom Board':
                        custom_config = self._load_custom_board()
                        if custom_config:
                            return custom_config
                        else:
                            return self.settings.DIFFICULTY_CONFIGS['Medium']
                    return self.settings.DIFFICULTY_CONFIGS.get(difficulty)
        return None

    def _load_custom_board(self) -> Optional[dict]:
        try:
            with open('custom_sudoku_board.txt', 'r') as f:
                puzzle = []
                for line in f:
                    line = line.strip()
                    if line:
                        puzzle.append([int(num) for num in line.split()])
                
                if len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
                    print("Error: Board must be 9x9")
                    return None
                
                solution = [row[:] for row in puzzle]
                from puzzle import PuzzleGenerator
                solver = PuzzleGenerator()
                if not solver._solve_grid(solution):
                    print("Error: Unsolvable puzzle")
                    return None
                
                zeros = sum(row.count(0) for row in puzzle)
                return {
                    'grid_size': 9,
                    'cells_removed': zeros,
                    'box_height': 3,
                    'box_width': 3,
                    'custom_puzzle': puzzle,
                    'custom_solution': solution
                }
                
        except Exception as e:
            print(f"Error loading custom board: {e}")
            return None

    def draw(self, screen: pygame.Surface):
        screen.fill(self.settings.BACKGROUND_COLOR)
        self._draw_sudoku_title(screen)

        for difficulty, rect in self.buttons.items():
            color = self.hover_color if difficulty == self._hovered_button else self.button_color
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, self.title_color, rect, 2, border_radius=10)

            if difficulty == "Load Custom Board":
                small_font = pygame.font.Font(None, 30)
                text_surface = small_font.render(difficulty, True, self.text_color)
            else:
                text_surface = self._font.render(difficulty, True, self.text_color)
            
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def _draw_sudoku_title(self, screen: pygame.Surface):
        title_text = self._title_font.render("Sudoku", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.settings.WINDOW_WIDTH // 2, 
                                           self.settings.WINDOW_HEIGHT // 4))

        shadow_text = self._title_font.render("Sudoku", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(title_rect.centerx + 3, 
                                       title_rect.centery + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)