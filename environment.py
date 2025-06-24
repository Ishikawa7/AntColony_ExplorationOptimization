import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
from ant import Ant
from scipy.ndimage import uniform_filter
from scipy.ndimage import maximum_filter
import threading

class Environment:
    def __init__(self, grid_size=25, n_goals=5, evaporation_rate=0.01, n_ants=100):
        self.ants = [Ant(grid_size) for _ in range(n_ants)]
        self.ants_map = np.zeros((grid_size, grid_size)) + 0.0
        for ant in self.ants:
            x, y = ant.position
            self.ants_map[x, y] = -10.0
        self.grid_size = grid_size
        self.n_goals = n_goals
        self.evaporation_rate = evaporation_rate
        # Initialize maps
        self.hot_positions_map = np.zeros((grid_size, grid_size)) + 0.0
        self.hot_positions = np.random.randint(0, grid_size, (n_goals, 2))
        for (i,j) in self.hot_positions:
            self.hot_positions_map[i, j] = 7.5
        self.map_pheromore =  np.zeros((grid_size, grid_size))+ 0.0

    def leave_pheromone(self, positions, pheromone_value):
            for position in positions:
                self.map_pheromore[position[0], position[1]] = pheromone_value
            
    def update_environment(self):
        self.map_pheromore = self.map_pheromore * (1 - self.evaporation_rate)
        self.map_pheromore = np.clip(self.map_pheromore, 0, 100)
        self.ants_map = np.zeros((self.grid_size, self.grid_size)) + 0.0
        for ant in self.ants:
            x, y = ant.position
            self.ants_map[x, y] = -10.0

    def step(self):
        for ant in self.ants:
            ant.move(self)
        self.update_environment()
    #def step(self):
    #    threads = []
    #    for ant in self.ants:
    #        thread = threading.Thread(target=ant.move, args=(self,))
    #        threads.append(thread)
    #        thread.start()
    #    # Wait for all threads to finish
    #    for thread in threads:
    #        thread.join()
    #    self.update_environment()

    def check_hot_positions(self, position):
        # Check if the position is in the hot positions
        if self.hot_positions_map[position[0], position[1]] > 1:
            self.hot_positions_map[position[0], position[1]] = -10.0
            return True
        elif self.hot_positions_map[position[0], position[1]] < -1:
            self.hot_positions_map[position[0], position[1]] = 10.0
            return False

    def render(self):
        clear_output(wait=True)
        # create the heatmaps
        # create four subplots, and display reward map, pheromone map, ants map, and hot positions map
        fig, axs = plt.subplots(2, 2, figsize=(14, 8))
        axs[0, 0].imshow(self.hot_positions_map + self.map_pheromore, cmap='bwr', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[0, 0].set_title('Hot Map')
        axs[0, 1].imshow(self.ants_map, cmap='binary', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[0, 1].set_title('Ants Map')
        # display the first ant maps
        # display the first ant exploration map
        axs[1, 0].imshow(self.ants[0].chosing_map, cmap='bwr', interpolation='nearest', aspect='auto', vmin=-10.0, vmax=10.0)
        axs[1, 0].set_title('Ant not visited Map')
        # display the first ant reward map
        axs[1, 1].imshow(self.ants[0].map_exploration, cmap='bwr', interpolation='nearest', aspect='auto', vmin=-20.0, vmax=20.0)
        axs[1, 1].set_title('Ant Exploration Map')
        plt.tight_layout()
        plt.show();