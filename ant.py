# ant.py
import numpy as np
from scipy.ndimage import maximum_filter, uniform_filter

class Ant:
    def __init__(self, grid_size=100):
        self.grid_size = grid_size
        self.reset()

    def reset(self):
        self.position = (
            np.random.randint(0, self.grid_size),
            np.random.randint(0, self.grid_size)
        )
        self.reward_map = np.ones((self.grid_size, self.grid_size))
        self.map_exploration = np.zeros((self.grid_size, self.grid_size))
        self.map_exploration[self.position] = -10.0
        self.pheromone_value = 0.0

    def get_q_star_map(self):
        combined = self.reward_map + self.map_exploration
        q_star_map = uniform_filter(
            maximum_filter(combined, size=3, mode='constant', cval=0.0),
            size=3, mode='constant', cval=0.0
        )
        return q_star_map

    def choose_action(self, q_star_map, epsilon=0.1):
        x, y = self.position
        x_min, x_max = max(0, x-1), min(self.grid_size, x+2)
        y_min, y_max = max(0, y-1), min(self.grid_size, y+2)

        local_map = q_star_map[x_min:x_max, y_min:y_max]
        local_shape = local_map.shape

        if np.random.rand() < epsilon:
            rand_idx = np.random.randint(0, local_shape[0]), np.random.randint(0, local_shape[1])
            next_pos = (x_min + rand_idx[0], y_min + rand_idx[1])
        else:
            max_idx = np.unravel_index(np.argmax(local_map), local_shape)
            next_pos = (x_min + max_idx[0], y_min + max_idx[1])

        return next_pos

    def update_maps(self, reward):
        self.reward_map[self.position] = reward
        self.map_exploration[self.position] = -10.0
        self.pheromone_value = -(reward ** 0.5)
        self.map_exploration *= 0.99
        self.reward_map = self.reward_map ** 0.99
