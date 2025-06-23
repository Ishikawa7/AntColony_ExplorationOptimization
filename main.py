# main.py
import time
import matplotlib.pyplot as plt
from environment_my import Environment

if __name__ == "__main__":
    env = Environment(grid_size=100, n_goals=10, n_ants=5)

    plt.ion()  # Enable interactive mode for real-time updates
    for step in range(100):
        env.step()
        env.render()
        print(f"Step {step + 1} completed.")
        time.sleep(0.1)

    plt.ioff()
    plt.show()