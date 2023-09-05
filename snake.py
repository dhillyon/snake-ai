import pygame
import sys
import random as r
import heapq

# Initialise Pygame
pygame.init()

# Constants
FPS = 10
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colour constants
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directional vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialise screeen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake AI")
font = pygame.font.Font(None, 36)

def update_grid(grid, x, y, value):
    grid[y][x] = value

# Spawns an apple in a random location
def init_apple(grid):
    apple = (r.randint(0, GRID_WIDTH - 1), r.randint(0, GRID_HEIGHT-1))
    
    # Ensure the apple can't spawn inside the snake
    while grid[apple[0]][apple[1]] == "snake":
        apple = (r.randint(0, GRID_WIDTH - 1), r.randint(0, GRID_HEIGHT-1))
    
    update_grid(grid, apple[0], apple[1], "apple")
    return apple

# Main game loop
def main(): 
    score = 0
    clock = pygame.time.Clock()
    run = True
    
    # Initialise grid. Used as a search space for the AI algorithm
    grid = [[None for _ in range(GRID_HEIGHT+1)] for _ in range(GRID_WIDTH+1)]
    
    # Initialise snake
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    update_grid(grid, snake[0][0], snake[0][1], "snake")
    snake_dir = RIGHT

    # Initialise apple
    apple = init_apple(grid)
    
    while run:
        # Set frame rate
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN: # Temp user input
                if event.key == pygame.K_UP and snake_dir != DOWN:
                    snake_dir = UP
                elif event.key == pygame.K_DOWN and snake_dir != UP:
                    snake_dir = DOWN
                elif event.key == pygame.K_LEFT and snake_dir != RIGHT:
                    snake_dir = LEFT
                elif event.key == pygame.K_RIGHT and snake_dir != LEFT:
                    snake_dir = RIGHT
            
        # Background colour
        screen.fill(WHITE)
        
        # Display score
        score_text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))
        
        ## Moving the snake
        # Remove previous snake from grid
        for segment in snake:
            update_grid(grid, segment[0], segment[1], None)
            
        # Update snake object
        head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, head)
        
        # Check if snake eats the apple
        if snake[0] == apple:
            apple = init_apple(grid)
            score += 1
        else:
            snake.pop()
        
        # Update grid
        for segment in snake:
            update_grid(grid, segment[0], segment[1], "snake")
        
        
        # Check if snake collides with the wall OR itself
        if (
            snake[0][0] < 0
            or snake[0][0] >= GRID_WIDTH
            or snake[0][1] < 0
            or snake[0][1] >= GRID_HEIGHT
            or snake[0] in snake[1:]
        ):
            run = False
        
        # Drawing the snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Drawing the apple
        pygame.draw.rect(screen, RED, (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        pygame.display.update()
     
    pygame.quit()
    print(grid)
    sys.exit()

if __name__ == "__main__":
    main()