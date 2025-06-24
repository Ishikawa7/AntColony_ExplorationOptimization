from scipy.ndimage import maximum_filter
from scipy.ndimage import uniform_filter
import numpy as np
import random
from copy import copy

class Ant:
    def __init__(self, grid_size=100):
        self.grid_size = grid_size
        # Initialize position randomly within the grid
        self.position = (np.random.randint(0, grid_size), np.random.randint(0, grid_size))
        self.map_exploration = np.zeros((grid_size, grid_size))
        self.not_visited_map = np.zeros((grid_size, grid_size)) + 1.0
        self.map_exploration[self.position] = -10.0
        self.not_visited_map[self.position] = 0.0
        self.pheromone_value = 1000.0  # Initial pheromone value
        self.chosing_map = np.zeros((grid_size, grid_size)) + 0.0
        self.last_hot_position = None
        self.direction = random.randint(0, 7)
        self.first = True

    def select_action(self, map):
        # Define 8 possible movement directions
        possible_directions = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]

        actions = {}
        for idx, direction in enumerate(possible_directions):
            new_x = self.position[0] + direction[0]
            new_y = self.position[1] + direction[1]

            # Check grid boundaries
            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                actions[direction] = map[new_x, new_y]

        total_value = sum(actions.values())
        if total_value <= 0.1:
            # Low confidence: stick to direction if possible, else pick random
            current_dir = possible_directions[self.direction]
            if current_dir not in actions:
                action = random.choice(list(actions.keys()))
                self.direction = possible_directions.index(action)
            else:
                action = current_dir
            if random.random() < 0.05:
                self.direction = random.randint(0, 7)  # Randomly change direction
        else:
            if random.random() < 0.3:
                action = random.choice(list(actions.keys()))
            else:
                action = max(actions, key=actions.get)
            # Update direction index
            self.direction = possible_directions.index(action)

        # Return the new position after taking action
        new_position = (self.position[0] + action[0], self.position[1] + action[1])
        return new_position
    
    def create_direct_path_between(self, start, end):
        # Create a direct path between start and end positions
        path = []
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return [start]
        for i in range(steps + 1):
            x = int(x1 + i * dx / steps)
            y = int(y1 + i * dy / steps)
            path.append((x, y))
        return path

    def move(self, env):
        self.map_exploration[self.position] = -100.0
        map = env.map_pheromore
        # update
        self.chosing_map = map# + self.map_exploration# + self.not_visited_map
        self.position = self.select_action(self.chosing_map)
        if env.check_hot_positions(self.position):
            if self.first:
                self.first = False
                self.last_hot_position = copy(self.position)
            else:
                # Leave pheromone on the path taken
                direct_path = self.create_direct_path_between(self.last_hot_position, self.position)
                env.leave_pheromone(direct_path, self.pheromone_value/len(direct_path))
                self.last_path = []
        self.not_visited_map[self.position] = 0.0
        self.map_exploration = self.map_exploration * 0.90
        #self.map_exploration = uniform_filter(self.map_exploration, size=2, mode='constant', cval=0.0)
        self.map_exploration = np.clip(self.map_exploration, -20.0, 20.0)