import pygame
import random
from settings import GameSettings

class VictoryScreen:
    def __init__(self, puzzle=None, solution=None):
        self.settings = GameSettings()
        self._font = pygame.font.Font(None, 80)
        self._small_font = pygame.font.Font(None, 40)
        self._particles = []
        self._create_particles()
        self.restart_button = pygame.Rect(
            self.settings.WINDOW_WIDTH // 2 - 100,
            self.settings.WINDOW_HEIGHT // 2 + 50,
            200, 60
        )
        self.puzzle = puzzle
        self.solution = solution
        self._has_saved = False

    def _create_particles(self):
        for _ in range(100):
            self._particles.append({
                'x': random.randint(0, self.settings.WINDOW_WIDTH),
                'y': random.randint(0, self.settings.WINDOW_HEIGHT),
                'speed': random.randint(2, 6),
                'size': random.randint(3, 8),
                'color': random.choice([
                    (255, 223, 0), (255, 215, 0), 
                    (0, 255, 255), (255, 100, 255), 
                    (100, 255, 100)
                ])
            })

    def update_particles(self):
        for particle in self._particles:
            particle['y'] += particle['speed']
            if particle['y'] > self.settings.WINDOW_HEIGHT:
                particle['y'] = -10
                particle['x'] = random.randint(0, self.settings.WINDOW_WIDTH)

    def save_solution(self):
        if self._has_saved or self.solution is None:
            return
            
        try:
            with open('custom_sudoku_board_solved.txt', 'w') as f:
                for row in self.solution:
                    f.write(' '.join(map(str, row)) + '\n')
            print("Saved solution to custom_sudoku_board_solved.txt")
            self._has_saved = True
        except Exception as e:
            print(f"Error saving solution: {e}")

    def draw(self, screen):
        if not self._has_saved:
            self.save_solution()

        overlay = pygame.Surface((self.settings.WINDOW_WIDTH, self.settings.WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        self.update_particles()
        for particle in self._particles:
            pygame.draw.circle(
                screen,
                particle['color'],
                (int(particle['x']), int(particle['y'])),
                particle['size']
            )

        text = self._font.render("YOU WIN!", True, (255, 255, 255))
        shadow = self._font.render("YOU WIN!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.settings.WINDOW_WIDTH // 2, 
                                      self.settings.WINDOW_HEIGHT // 2 - 50))

        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (40, 80, 120), self.restart_button, border_radius=10)
        pygame.draw.rect(screen, (60, 120, 180), self.restart_button, 3, border_radius=10)

        restart_text = self._small_font.render("Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=self.restart_button.center)
        screen.blit(restart_text, restart_rect)

    def check_restart_click(self, pos):
        return self.restart_button.collidepoint(pos)