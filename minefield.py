import random
from constants import *

class Minefield:
    def __init__(self, difficulty):
        self.grid_size = GRID_SIZE
        self.board = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.flags = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.game_over = False
        self.won = False
        
        # Set mines based on difficulty
        mine_counts = {"easy": 40, "medium": 60, "hard": 80}
        self.place_mines(mine_counts[difficulty])
        
    def place_mines(self, count):
        mines_placed = 0
        while mines_placed < count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1
                self.update_numbers(x, y)
    
    def update_numbers(self, mine_x, mine_y):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = mine_x + dx, mine_y + dy
                if (0 <= new_x < self.grid_size and 
                    0 <= new_y < self.grid_size and 
                    self.board[new_y][new_x] != -1):
                    self.board[new_y][new_x] += 1
    
    def reveal(self, x, y):
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return
        if self.revealed[y][x] or self.flags[y][x]:
            return
        
        self.revealed[y][x] = True
        
        if self.board[y][x] == -1:
            self.game_over = True
            return
        
        if self.board[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    self.reveal(x + dx, y + dy)
        
        # Check for win
        unrevealed = sum(row.count(False) for row in self.revealed)
        mine_count = sum(row.count(-1) for row in self.board)
        if unrevealed == mine_count:
            self.won = True
    
    def toggle_flag(self, x, y):
        if not self.revealed[y][x]:
            self.flags[y][x] = not self.flags[y][x]