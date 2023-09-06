import pygame
import sys
import random as r
import heapq

# Initialise Pygame
pygame.init()

# Constants
FPS = 40
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
MAX_TICKS_WITHOUT_PATH = 1

# Colour constants
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directional vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialise screeen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake AI")
font = pygame.font.Font(None, 36)

# Main game loop
def main(): 
    score = 0
    clock = pygame.time.Clock()
    run = True
    ticks_without_path = 0
    
    # Initialise grid. Used as a search space for the AI algorithm
    grid = [[None for _ in range(GRID_HEIGHT+1)] for _ in range(GRID_WIDTH+1)]
    
    # Initialise snake
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    update_grid(grid, snake[0][0], snake[0][1], "snake")
    snake_dir = RIGHT

    # Initialise apple
    apple = init_apple(grid, snake)
    
    while run:
        # Set frame rate
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        path = dijkstra(grid, snake[0], apple, snake)

        if path != []:
            ticks_without_path = 0
            next_move = (path[0][0] - snake[0][0], path[0][1] - snake[0][1])
        else:
            # No path is found. Increment tick counter
            ticks_without_path += 1
            
            # Snake has had no path for too long. Find valid moves until a path opens up. 
            if ticks_without_path >= MAX_TICKS_WITHOUT_PATH:
                next_cell = find_best_empty_cell(grid, snake, snake_dir)
                next_move = (next_cell[0] - snake[0][0], next_cell[1] - snake[0][1])
            
        snake_dir = next_move
        
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
            apple = init_apple(grid, snake)
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
            if segment == snake[0]: # Head
                pygame.draw.rect(screen, BLUE, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)) #Head
            else:
                pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Drawing the apple
        pygame.draw.rect(screen, RED, (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        pygame.display.update()
     
    pygame.quit()
    sys.exit()

# Simple implementation of Dijkstras algorithm. Finds shortest path from start to goal in grid.
def dijkstra(grid, start, goal, snake):
    # Init the fringe set with start node
    fringe_set = [(0, start)]
    heapq.heapify(fringe_set)
    came_from = {}
    
    # Init costs
    cost = {(x, y): float('inf') for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
    cost[start] = 0
    
    while fringe_set:
        _, current_node = heapq.heappop(fringe_set)
        
        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            
            path.reverse()
            return path

        for move in [UP, DOWN, LEFT, RIGHT]:
            neighbour = (current_node[0] + move[0], current_node[1] + move[1])
            
            if (
                0 <= neighbour[0] < GRID_WIDTH
                and 0 <= neighbour[1] < GRID_HEIGHT
                and (neighbour[0], neighbour[1]) not in snake # Avoid snake body
            ):
                tentative_cost = cost[current_node] + 1
                
                if tentative_cost < cost[neighbour]:
                    came_from[neighbour] = current_node
                    cost[neighbour] = tentative_cost
                    heapq.heappush(fringe_set, (cost[neighbour], neighbour))
        
    return [] # No path

# For use when there is no valid path to food. Finds best fitting neighbour cell, based on
# longest valid empty path from snake
def find_best_empty_cell(grid, snake, snake_dir):
    head = snake[0]
    
    longest_path = -1
    best_move = (head[0] + snake_dir[0], head[1] + snake_dir[1]) # Best CURRENTLY KNOWN move
    
    for move in [UP, RIGHT, DOWN, LEFT]:
        neighbour = (head[0] + move[0], head[1] + move[1])
        
        # Check if neighbour is valid
        if (
            0 <= neighbour[0] < GRID_WIDTH
            and 0 <= neighbour[1] < GRID_WIDTH
            and (neighbour[0], neighbour[1]) not in snake
        ):
            path_length = calculate_potential_path_length(snake, grid, neighbour)
            if path_length > longest_path:
                longest_path = path_length
                best_move = neighbour
    
    # Returns best fitting neighbour cell
    return best_move           

# A modified version of the Dijkstra function which returns the length of the
# longest empty path from the snake
def calculate_potential_path_length(grid, snake, start):
    # Init fringe set with start node
    fringe_set = [(0, start)]
    heapq.heapify(fringe_set)
    
    # Init costs
    cost = {(x, y): float('inf') for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
    cost[start] = 0
    
    potential_path_length = 0
    
    while fringe_set:
        _, current = heapq.heappop(fringe_set)
        
        for move in (UP, RIGHT, DOWN, LEFT):
            neighbour = (current[0] + move[0], current[1] + move[1])
            
            # Check if neighbour is valid
            if (
                0 <= neighbour[0] < GRID_WIDTH
                and 0 <= neighbour[1] < GRID_WIDTH
                and (neighbour[0], neighbour[1]) not in snake
            ):
                tentative_cost = cost[current] + 1
                
                if tentative_cost < cost[neighbour]:
                    cost[neighbour] = tentative_cost
                    heapq.heappush(fringe_set, (cost[neighbour], neighbour))
                
        if cost[current] > potential_path_length:
            potential_path_length = cost[current]
    
    return potential_path_length

# Self explanatory
def update_grid(grid, x, y, value):
    grid[y][x] = value

# Spawns an apple in a random location
def init_apple(grid, snake):
    apple = (r.randint(0, GRID_WIDTH - 1), r.randint(0, GRID_HEIGHT-1))
    
    # Ensure the apple can't spawn inside the snake
    while apple in snake:
        apple = (r.randint(0, GRID_WIDTH - 1), r.randint(0, GRID_HEIGHT-1))
    
    update_grid(grid, apple[0], apple[1], "apple")
    return apple

if __name__ == "__main__":
    main()
