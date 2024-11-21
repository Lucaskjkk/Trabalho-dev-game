import pygame
from constants import *
from minefield import Minefield

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Minefield")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.difficulties = ["easy", "medium", "hard"]
        self.current_difficulty_index = 0
        self.difficulty = self.difficulties[self.current_difficulty_index]
        self.minefield = None
        self.state = "menu"
    
    def draw_menu(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title_text = self.font.render("Minefield", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(WINDOW_SIZE//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw difficulty options
        for i, diff in enumerate(self.difficulties):
            # Highlight selected difficulty
            if diff == self.difficulty:
                # Draw selection box
                text = self.font.render(diff.title(), True, (0, 255, 0))
                rect = text.get_rect(center=(WINDOW_SIZE//2, 250 + i*60))
                # Draw highlight box
                highlight_rect = rect.inflate(20, 10)
                pygame.draw.rect(self.screen, (0, 200, 0), highlight_rect, 2, border_radius=5)
            else:
                text = self.font.render(diff.title(), True, (100, 100, 100))
                rect = text.get_rect(center=(WINDOW_SIZE//2, 250 + i*60))
            
            self.screen.blit(text, rect)
        
        # Draw instructions
        instructions = [
            "↑/↓ - Select Difficulty",
            "SPACE - Start Game",
            "Left Click - Reveal Cell",
            "Right Click - Flag Mine"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, (50, 50, 50))
            rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE - 150 + i*30))
            self.screen.blit(text, rect)
    
    def draw_cell(self, x, y):
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        if not self.minefield.revealed[y][x]:
            # Draw covered cell
            pygame.draw.rect(self.screen, COVERED_COLOR, rect)
            pygame.draw.rect(self.screen, BORDER_COLOR, rect, 1)
            
            # Draw flag if present
            if self.minefield.flags[y][x]:
                flag_points = [
                    (x * CELL_SIZE + CELL_SIZE//4, y * CELL_SIZE + CELL_SIZE//4),
                    (x * CELL_SIZE + CELL_SIZE//4, y * CELL_SIZE + CELL_SIZE*3//4),
                    (x * CELL_SIZE + CELL_SIZE*3//4, y * CELL_SIZE + CELL_SIZE//2)
                ]
                pygame.draw.polygon(self.screen, FLAG_COLOR, flag_points)
        else:
            # Draw revealed cell
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, rect)
            pygame.draw.rect(self.screen, BORDER_COLOR, rect, 1)
            
            if self.minefield.board[y][x] == -1:
                # Draw mine
                center = (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2)
                pygame.draw.circle(self.screen, MINE_COLOR, center, CELL_SIZE//3)
            elif self.minefield.board[y][x] > 0:
                # Draw number
                text = self.font.render(str(self.minefield.board[y][x]), True,
                                      MINE_COLORS[self.minefield.board[y][x]])
                text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE//2,
                                                y * CELL_SIZE + CELL_SIZE//2))
                self.screen.blit(text, text_rect)
    
    def draw_game(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw grid
        for y in range(self.minefield.grid_size):
            for x in range(self.minefield.grid_size):
                self.draw_cell(x, y)
        
        # Draw status bar
        status_rect = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, 100)
        pygame.draw.rect(self.screen, STATUS_BAR_COLOR, status_rect)
        
        if self.minefield.game_over:
            text = self.font.render("Game Over! Press R to Restart", True, MINE_COLOR)
        elif self.minefield.won:
            text = self.font.render("You Won! Press R to Restart", True, (0, 255, 0))
        else:
            text = self.font.render(f"Difficulty: {self.difficulty.title()}", True, (0, 0, 0))
        
        text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE + 50))
        self.screen.blit(text, text_rect)
    
    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_difficulty_index = (self.current_difficulty_index - 1) % len(self.difficulties)
                self.difficulty = self.difficulties[self.current_difficulty_index]
            elif event.key == pygame.K_DOWN:
                self.current_difficulty_index = (self.current_difficulty_index + 1) % len(self.difficulties)
                self.difficulty = self.difficulties[self.current_difficulty_index]
            elif event.key == pygame.K_SPACE:
                self.minefield = Minefield(self.difficulty)
                self.state = "game"
    
    def handle_game_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.state = "menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
            if y < GRID_SIZE:  # Ensure click is within grid
                if event.button == 1:  # Left click
                    self.minefield.reveal(x, y)
                elif event.button == 3:  # Right click
                    self.minefield.toggle_flag(x, y)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.state == "menu":
                    self.handle_menu_input(event)
                else:
                    self.handle_game_input(event)
            
            if self.state == "menu":
                self.draw_menu()
            else:
                self.draw_game()
            
            pygame.display.flip()
            self.clock.tick(60)