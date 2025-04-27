import pygame
from settings import GameSettings

class GameControls:
    def __init__(self):
        self.settings = GameSettings()
        self._font = pygame.font.Font(None, 30)
        self.button_width = 150
        self.button_height = 50
        self.button_margin = 20
        
        total_width = 4 * self.button_width + 3 * self.button_margin
        buttons_x = (self.settings.WINDOW_WIDTH - total_width) // 2

        self.menu_button = pygame.Rect(
            buttons_x,
            self.settings.CONTROL_PANEL_HEIGHT // 2 - self.button_height // 2,
            self.button_width,
            self.button_height
        )

        self.exit_button = pygame.Rect(
            buttons_x + self.button_width + self.button_margin,
            self.settings.CONTROL_PANEL_HEIGHT // 2 - self.button_height // 2,
            self.button_width,
            self.button_height
        )

        self.check_button = pygame.Rect(
            buttons_x + 2 * (self.button_width + self.button_margin),
            self.settings.CONTROL_PANEL_HEIGHT // 2 - self.button_height // 2,
            self.button_width,
            self.button_height
        )

        self.clear_button = pygame.Rect(
            buttons_x + 3 * (self.button_width + self.button_margin),
            self.settings.CONTROL_PANEL_HEIGHT // 2 - self.button_height // 2,
            self.button_width,
            self.button_height
        )

        self.button_color = (40, 60, 100)
        self.hover_color = (60, 80, 120)
        self.text_color = (255, 255, 255)
        self.title_color = (0, 200, 255)
        self._hovered_button = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.settings.PANEL_COLOR,
                        (0, 0, self.settings.WINDOW_WIDTH, self.settings.CONTROL_PANEL_HEIGHT))

        self._draw_button(screen, self.menu_button, "Menu")
        self._draw_button(screen, self.exit_button, "Exit")
        self._draw_button(screen, self.check_button, "Check")
        self._draw_button(screen, self.clear_button, "Clear")

    def _draw_button(self, screen, button_rect, text):
        color = self.hover_color if button_rect == self._hovered_button else self.button_color
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        pygame.draw.rect(screen, self.title_color, button_rect, 2, border_radius=10)

        text_surface = self._font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self._hovered_button = None
            if self.menu_button.collidepoint(mouse_pos):
                self._hovered_button = self.menu_button
            elif self.exit_button.collidepoint(mouse_pos):
                self._hovered_button = self.exit_button
            elif self.check_button.collidepoint(mouse_pos):
                self._hovered_button = self.check_button
            elif self.clear_button.collidepoint(mouse_pos):
                self._hovered_button = self.clear_button

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.menu_button.collidepoint(mouse_pos):
                return 'menu'
            elif self.exit_button.collidepoint(mouse_pos):
                return 'exit'
            elif self.check_button.collidepoint(mouse_pos):
                return 'check'
            elif self.clear_button.collidepoint(mouse_pos):
                return 'clear'
        return None