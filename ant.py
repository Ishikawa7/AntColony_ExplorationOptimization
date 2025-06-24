from scipy.ndimage import maximum_filter
from scipy.ndimage import uniform_filter
import numpy as np

class Ant:
    def __init__(self, grid_size=100, learning_rate=0.5, discount_factor=0.9):
        self.grid_size = grid_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        # Initialize position randomly within the grid
        self.position = (np.random.randint(0, grid_size), np.random.randint(0, grid_size))
        self.reward_map =  np.zeros((grid_size, grid_size)) + 0.0
        self.map_exploration = np.zeros((grid_size, grid_size)) + 1.0
        self.map_exploration[self.position] = -10.0  # Initial exploration value at the ant's position
        self.pheromone_value = 0.0  # Initial pheromone value
        self.q_star_map = np.random.rand(grid_size, grid_size)  # Initialize q_star_map

    def select_action(self, map):
        # Select the action with the highest value in q_star_map at the ant's current position
        positions = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]
        actions = {}
        for pos in positions:
            new_x = self.position[0] + pos[0]
            new_y = self.position[1] + pos[1]
            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                actions[pos] = map[new_x, new_y]
        # get the action with the maximum value
        best_action = max(actions, key=actions.get)
        new_position = (self.position[0] + best_action[0], self.position[1] + best_action[1])
        return new_position

    def move(self, env):
        # update exploration map
        self.map_exploration[self.position] = -10.0
        # update environment with pheromone value
        self.pheromone_value *= 0.9  # Decay pheromone value
        self.pheromone_value = np.clip(self.pheromone_value, -2.5, 2.5)
        env.leave_pheromone(self.position, self.pheromone_value)
        # calculate q_star_map
        estimate_q = uniform_filter(maximum_filter(self.reward_map, size=3, mode='constant', cval=0.0), size=3, mode='constant', cval=0.0)
        self.q_star_map = (1 - self.learning_rate) * self.q_star_map + self.learning_rate * (self.reward_map + self.discount_factor * estimate_q)

        q_star_map_ponderated = self.q_star_map.copy() + self.map_exploration
        # update position
        self.position = self.select_action(q_star_map_ponderated)
        # update reward map
        reward = env.get_reward(self.position)
        self.reward_map[self.position] = reward
        if reward > 0:
            self.map_exploration[self.position] = -reward*2  # Update exploration value at the new position
        # update pheromone value
        self.pheromone_value += reward
        # cap the pheromone value from -1.0 to 1.0
        self.pheromone_value = np.clip(self.pheromone_value, -1.0, 1.0)
        # decay exploration map
        self.map_exploration = self.map_exploration * 0.99
        # clip the exploration map between -10.0 and 10
        self.map_exploration = np.clip(self.map_exploration, -10.0, 10.0)
        # decay reward map
        self.reward_map = self.reward_map * 0.99
        # clip the reward map between -10.0 and 10.0
        self.reward_map = np.clip(self.reward_map, -10.0, 10.0)