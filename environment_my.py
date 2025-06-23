import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
from ant_my import Ant

class Environment:
    def __init__(self, grid_size=100, n_goals=10, evaporation_rate=0.1, n_ants=5):
        self.ants = [Ant(grid_size) for _ in range(n_ants)]
        self.ants_map = np.zeros((grid_size, grid_size)) + 0.0
        for ant in self.ants:
            x, y = ant.position
            self.ants_map[x, y] = -10.0
        self.grid_size = grid_size
        self.n_goals = n_goals
        self.evaporation_rate = evaporation_rate
        # state is a 2D numpy array representing the grid
        self.reward_map =  np.zeros((grid_size, grid_size)) + 0.0
        self.hot_positions_map = np.zeros((grid_size, grid_size)) + 0.0
        self.hot_positions = np.random.randint(0, grid_size, (n_goals, 2))
        for (i,j) in self.hot_positions:
            self.hot_positions_map[i, j] = 5.0
        self.map_pheromore =  np.zeros((grid_size, grid_size))+ 0.0
        self.reward_map = self.reward_map + self.map_pheromore + self.hot_positions_map
        #self._lock = threading.Lock()

    def reset(self):
        self.reward_map = np.zeros((self.grid_size, self.grid_size)) + 0.0
        self.map_pheromore = np.zeros((self.grid_size, self.grid_size)) + 0.0
        self.hot_positions_map = np.zeros((self.grid_size, self.grid_size)) + 0.0
        for (i,j) in self.hot_positions:
            self.hot_positions_map[i, j] = 5.0
        self.reward_map = self.reward_map + self.map_pheromore + self.hot_positions_map
        for ant in self.ants:
            ant.reset()

    def leave_pheromone(self, position, pheromone_value=0):
        #with self._lock:
            x, y = position
            self.map_pheromore[x, y] += pheromone_value
            self.reward_map = self.reward_map + self.map_pheromore * (1 -self.evaporation_rate)
    
    def update_environment(self):
        #with self._lock:
        self.map_pheromore = self.map_pheromore * (1 - self.evaporation_rate)

    def step(self):
        #with self._lock:
        for ant in self.ants:
            ant.move(self)
        self.update_environment()
        # update ants map
        self.ants_map = np.zeros((self.grid_size, self.grid_size)) + 1.0
        for ant in self.ants:
            x, y = ant.position
            self.ants_map[x, y] += 0.0

    def get_reward(self, position):
        #with self._lock:
            x, y = position
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                return self.reward_map[x, y]
            else:
                return 0
            
    def render(self):
        clear_output(wait=True)
        # create the heatmap
        plt.imshow(self.reward_map+self.map_pheromore+self.ants_map, cmap='hot', interpolation='nearest', aspect='auto')
        plt.show();