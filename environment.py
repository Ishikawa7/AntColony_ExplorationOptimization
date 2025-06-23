# environment.py
import numpy as np
import matplotlib.pyplot as plt
import time
from ant import Ant

class Environment:
    def __init__(self, grid_size=100, n_goals=10, evaporation_rate=0.1, n_ants=5):
        self.grid_size = grid_size
        self.n_goals = n_goals
        self.evaporation_rate = evaporation_rate
        self.ants = [Ant(grid_size) for _ in range(n_ants)]

        self.map_pheromone = np.zeros((grid_size, grid_size))
        self.hot_positions_map = np.zeros((grid_size, grid_size))
        self.ants_map = np.zeros((grid_size, grid_size))

        self.hot_positions = np.random.randint(0, grid_size, (n_goals, 2))
        for i, j in self.hot_positions:
            self.hot_positions_map[i, j] = 5.0

        self.update_reward_map()

    def update_reward_map(self):
        self.reward_map = self.map_pheromone + self.hot_positions_map

    def reset(self):
        self.map_pheromone.fill(0.0)
        self.hot_positions_map.fill(0.0)
        for i, j in self.hot_positions:
            self.hot_positions_map[i, j] = 5.0

        for ant in self.ants:
            ant.reset()

        self.update_reward_map()

    def leave_pheromone(self, position, pheromone_value):
        x, y = position
        self.map_pheromone[x, y] += pheromone_value

    def update_environment(self):
        self.map_pheromone *= (1 - self.evaporation_rate)

    def step(self):
        for ant in self.ants:
            q_star_map = ant.get_q_star_map()
            new_pos = ant.choose_action(q_star_map)
            ant.position = new_pos
            reward = self.get_reward(new_pos)
            ant.update_maps(reward)
            self.leave_pheromone(new_pos, ant.pheromone_value)

        self.update_environment()
        self.update_reward_map()
        self.update_ants_map()

    def update_ants_map(self):
        self.ants_map.fill(0.0)
        for ant in self.ants:
            x, y = ant.position
            self.ants_map[x, y] = -10.0

    def get_reward(self, position):
        x, y = position
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.reward_map[x, y]
        return 0.0

    def render(self):
        plt.imshow(self.reward_map + self.ants_map, cmap='hot', interpolation='nearest')
        plt.title("Ant Simulation")
        plt.pause(0.01)
        plt.clf()