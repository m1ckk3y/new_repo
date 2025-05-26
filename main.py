import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetromino:
    def __init__(self):
        self.shape = random.randint(0, len(SHAPES) - 1)
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - len(SHAPES[self.shape][0]) // 2
        self.y = 0
        self.color = COLORS[self.shape]

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.game_over = False
        self.score = 0

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.grid[y][x],
                               (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.screen, WHITE,
                               (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_current_piece(self):
        shape = SHAPES[self.current_piece.shape]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    pygame.draw.rect(self.screen, self.current_piece.color,
                                   ((self.current_piece.x + x) * BLOCK_SIZE,
                                    (self.current_piece.y + y) * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE), 0)

    def move_piece(self, dx, dy):
        self.current_piece.x += dx
        self.current_piece.y += dy
        if not self.valid_move():
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            if dy > 0:
                self.freeze_piece()
                self.clear_lines()
                self.current_piece = Tetromino()
                if not self.valid_move():
                    self.game_over = True

    def valid_move(self):
        shape = SHAPES[self.current_piece.shape]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    if (self.current_piece.x + x < 0 or
                        self.current_piece.x + x >= GRID_WIDTH or
                        self.current_piece.y + y >= GRID_HEIGHT or
                        self.grid[self.current_piece.y + y][self.current_piece.x + x] != BLACK):
                        return False
        return True

    def freeze_piece(self):
        shape = SHAPES[self.current_piece.shape]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color

    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if all(color != BLACK for color in self.grid[y]):
                lines_cleared += 1
                del self.grid[y]
                self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        self.score += lines_cleared * 100

    def run(self):
        fall_time = 0
        fall_speed = 0.5  # seconds
        
        while not self.game_over:
            fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        if not self.valid_move():
                            self.current_piece.rotation = (self.current_piece.rotation - 1) % 4

            if fall_time >= fall_speed * 1000:
                self.move_piece(0, 1)
                fall_time = 0

            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_current_piece()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()