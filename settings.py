class GameTheme:
    BACKGROUND_COLOR = (10, 15, 30)
    PANEL_COLOR = (10, 15, 30)
    GRID_BG_COLOR = (15, 25, 45)
    GRID_LINE_COLOR = (0, 200, 255)
    HIGHLIGHT_COLOR = (0, 150, 150, 50)
    BUTTON_COLOR = (0, 100, 200)
    BUTTON_HOVER_COLOR = (0, 150, 255)
    TEXT_COLOR = (0, 255, 255)
    ERROR_COLOR = (255, 50, 50)
    SUCCESS_COLOR = (0, 255, 180)
    SELECTED_COLOR = (6, 8, 15)
    INPUT_COLOR = (200, 255, 255)

class GameSettings:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 900
        self.MARGIN = 40
        self.BACKGROUND_COLOR = GameTheme.BACKGROUND_COLOR
        self.GRID_LINE_COLOR = GameTheme.GRID_LINE_COLOR
        self.GRID_BG_COLOR = GameTheme.GRID_BG_COLOR
        self.HIGHLIGHT_COLOR = GameTheme.HIGHLIGHT_COLOR
        self.TEXT_COLOR = GameTheme.TEXT_COLOR
        self.ERROR_COLOR = GameTheme.ERROR_COLOR
        self.SUCCESS_COLOR = GameTheme.SUCCESS_COLOR
        self.BUTTON_COLOR = GameTheme.BUTTON_COLOR
        self.BUTTON_HOVER_COLOR = GameTheme.BUTTON_HOVER_COLOR
        self.PANEL_COLOR = GameTheme.PANEL_COLOR
        self.CONTROL_PANEL_HEIGHT = 100
        self.CONTROL_PANEL_MARGIN = 30
        self.GRID_SIZE = 9
        self.TOTAL_GRID_SIZE = 720
        self.CELL_SIZE = self.TOTAL_GRID_SIZE // self.GRID_SIZE
        self.GRID_OFFSET_X = (self.WINDOW_WIDTH - self.TOTAL_GRID_SIZE) // 2
        self.GRID_OFFSET_Y = self.CONTROL_PANEL_HEIGHT + self.CONTROL_PANEL_MARGIN + 10
        
        self.DIFFICULTY_CONFIGS = {
            'Easy': {'grid_size': 9, 'cells_removed': 10, 'box_height': 3, 'box_width': 3},
            'Medium': {'grid_size': 9, 'cells_removed': 30, 'box_height': 3, 'box_width': 3},
            'Hard': {'grid_size': 9, 'cells_removed': 45, 'box_height': 3, 'box_width': 3}
        }

    def update_grid_size(self, grid_size: int):
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = self.TOTAL_GRID_SIZE // self.GRID_SIZE
        self.GRID_OFFSET_X = (self.WINDOW_WIDTH - self.TOTAL_GRID_SIZE) // 2
        self.GRID_OFFSET_Y = self.CONTROL_PANEL_HEIGHT + self.CONTROL_PANEL_MARGIN + 10