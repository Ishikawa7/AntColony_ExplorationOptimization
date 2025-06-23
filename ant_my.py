from scipy.ndimage import maximum_filter
from scipy.ndimage import uniform_filter
import numpy as np

class Ant:
    def __init__(self, grid_size=100):
        self.grid_size = grid_size
        self.position = (np.random.randint(0, grid_size), np.random.randint(0, grid_size))
        self.reward_map =  np.zeros((grid_size, grid_size)) + 1.0
        self.map_exploration = np.zeros((grid_size, grid_size)) + 10.0
        self.map_exploration[self.position] = -10.0  # Initial exploration value at the ant's position
        self.pheromone_value = 0.0  # Initial pheromone value

    def reset(self):
        self.position = (np.random.randint(0, self.grid_size), np.random.randint(0, self.grid_size))
        self.reward_map = np.zeros((self.grid_size, self.grid_size)) + 1.0
        self.map_exploration = np.zeros((self.grid_size, self.grid_size)) + 0.0
        self.map_exploration[self.position] = -10.0  # Reset exploration value at the ant's position
        self.pheromone_value = 0.0

    def move(self, env):
        # calculate q_star_map
        q_star_map = uniform_filter(maximum_filter(self.reward_map + self.map_exploration, size=3, mode='constant', cval=0.0), size=3, mode='constant', cval=0.0)
        # get the best action: best position to move to from current position
        old_position = self.position
        x, y = old_position
        best_action = np.unravel_index(np.argmax(q_star_map[x-1:x+2, y-1:y+2]), (3, 3)) #IMPLEMENT STOCHASTICITY!
        best_action = (best_action[0] + x - 1, best_action[1] + y - 1)
        # bound check
        best_action = (max(0, min(self.grid_size - 1, best_action[0])), max(0, min(self.grid_size - 1, best_action[1])))
        # update position
        self.position = best_action
        # update reward map
        reward = env.get_reward(self.position)
        self.reward_map[self.position] = reward
        # update exploration map
        self.map_exploration[self.position] = -10.0
        # update pheromone value
        self.pheromone_value = -(reward**0.5)
        # update environment with pheromone value
        env.leave_pheromone(self.position, self.pheromone_value)
        # decay exploration map
        self.map_exploration = self.map_exploration * 0.99
        # decay reward map
        self.reward_map = self.reward_map ** 0.99