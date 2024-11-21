import pygame

# Window and Grid
WINDOW_SIZE = 800
GRID_SIZE = 20
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colors
COVERED_COLOR = (169, 169, 169)  # Dark gray for covered cells
BORDER_COLOR = (120, 120, 120)   # Darker gray for borders
MINE_COLOR = (255, 0, 0)         # Red for mines
FLAG_COLOR = (255, 0, 0)         # Red for flags
BACKGROUND_COLOR = (200, 200, 200)
STATUS_BAR_COLOR = (150, 150, 150)

# Number colors
MINE_COLORS = {
    1: (0, 0, 255),      # Blue
    2: (0, 128, 0),      # Green
    3: (255, 0, 0),      # Red
    4: (0, 0, 128),      # Dark Blue
    5: (128, 0, 0),      # Dark Red
    6: (0, 128, 128),    # Teal
    7: (0, 0, 0),        # Black
    8: (128, 128, 128)   # Gray
}