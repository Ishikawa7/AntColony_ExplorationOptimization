import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
from ant import Ant

class Environment:
    def __init__(self, grid_size=25, n_goals=10, evaporation_rate=0.1, n_ants=5):
        self.ants = [Ant(grid_size) for _ in range(n_ants)]
        self.ants_map = np.zeros((grid_size, grid_size)) + 0.0
        for ant in self.ants:
            x, y = ant.position
            self.ants_map[x, y] = -10.0

        self.grid_size = grid_size
        self.n_goals = n_goals
        self.evaporation_rate = evaporation_rate
        # Initialize maps
        self.reward_map =  np.zeros((grid_size, grid_size)) - 0.5
        self.hot_positions_map = np.zeros((grid_size, grid_size)) + 0.0
        self.hot_positions = np.random.randint(0, grid_size, (n_goals, 2))
        for (i,j) in self.hot_positions:
            self.hot_positions_map[i, j] = 5.5
        self.map_pheromore =  np.zeros((grid_size, grid_size))+ 0.0
        self.reward_map = self.reward_map + self.map_pheromore + self.hot_positions_map

    def leave_pheromone(self, position, pheromone_value=0):
            x, y = position
            self.map_pheromore[x, y] += pheromone_value

    def get_reward(self, position):
            x, y = position
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                return self.reward_map[x, y]
            else:
                return 0
    
    def update_environment(self):
        self.map_pheromore = self.map_pheromore * (1 - self.evaporation_rate)
        # cap the pheromone map to a maximum from -2.0 to 2.0
        self.map_pheromore = np.clip(self.map_pheromore, -2.5, 2.5)
        self.reward_map = (np.zeros((self.grid_size, self.grid_size)) - 0.5 + self.map_pheromore + self.hot_positions_map)
        self.ants_map = np.zeros((self.grid_size, self.grid_size)) + 0.0
        for ant in self.ants:
            x, y = ant.position
            self.ants_map[x, y] = -10.0
            
    def step(self):
        for ant in self.ants:
            ant.move(self)
        self.update_environment()

    def render(self):
        clear_output(wait=True)
        # create the heatmaps
        # create four subplots, and display reward map, pheromone map, ants map, and hot positions map
        fig, axs = plt.subplots(2, 3, figsize=(10, 10))
        axs[0, 0].imshow(self.reward_map, cmap='bwr', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[0, 0].set_title('Reward Map')
        axs[0, 1].imshow(self.map_pheromore, cmap='PRGn', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[0, 1].set_title('Pheromone Map')
        axs[0, 2].imshow(self.ants_map, cmap='binary', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[0, 2].set_title('Ants Map')
        # display the first ant maps
        # display the first ant exploration map
        axs[1, 0].imshow(self.ants[0].reward_map, cmap='bwr', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[1, 0].set_title('Ant Reward Map')
        # display the first ant reward map
        axs[1, 1].imshow(self.ants[0].map_exploration, cmap='bwr', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[1, 1].set_title('Ant Exploration Map')
        # display the first ant q_star_map
        axs[1, 2].imshow(self.ants[0].q_star_map, cmap='Greens', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[1, 2].set_title('Ant Q* Map')
        plt.tight_layout()
        plt.show();