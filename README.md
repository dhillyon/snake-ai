# snake-ai
Basic AI path finding concepts are applied to play and beat the game "Snake". The game is build using the [Pygame](https://www.pygame.org/docs/) module.

Currently the snake's behaviour is implemented via [Dijkstra's](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) path-finding algorithm however I intend on adding an option for an [A* algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) in the future.

## Run locally
1. Fork the repository by clicking on `Fork` option on the top right of the repository.
2. Open a terminal on your local computer.
3. Clone the forked repository by adding your own GitHub username in place of `<username>`.
   ```
   git clone https://github.com/<username>/snake-ai
   ```
4. Navigate to the cloned respository.
5. Install dependencies.
   ```
   pip install requirements.txt
   ```
6. Run the game using `python snake.py` or `python3 snake.py`

## Demo
![Demo](https://github.com/dbarrett4/snake-ai/blob/8bcb572944eaf4cad8b43befbb95c081d3f99dc1/snakedemo.gif)

## How it works
- Once per tick (frame):
   1. The shortest path from the snakes head to the apple is found (if any).
      - Sometimes there is no path. The apple may spawn in a section of the grid cut off by the snakes body, as an example.
      - In such cases, the snake finds the longest possible path of empty cells in an attempt to stay alive for as long as possible or until a path to the apple opens up.
      - Continues as per below with that path.
   2. The snake uses the co-ordinates of the first cell on that path and the co-ordinates of it's head to calculate it's direction vector, stored as `snake_dir`.
   3. The snake moves one cell in the direction indicated by the `snake_dir` vector.
