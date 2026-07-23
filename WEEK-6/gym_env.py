import gymnasium as gym
import numpy as np

class RL_Arena_Env(gym.Env):

    def __init__(self, grid_size=15):
        super().__init__()
        self.grid_size = grid_size
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(grid_size, grid_size, 4), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(4)
        self.max_steps = 300

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.steps = 0

        # Enemy
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        enemy_territory = [(6, 10), (6, 11), (6, 12),
                            (7, 10), (7, 11), (7, 12),
                            (8, 10), (8, 11), (8, 12),
                            (9, 10), (9, 11), (9, 12), 
                            (10,10), (10,11), (10,12), 
                            (11,10), (11,11), (11,12)]
        for (r, c) in enemy_territory:
            self.grid[r][c] = 2
        enemy_trail = [(12, 11), (13, 11), (13, 10), (13, 9), (13, 8), (13, 7), (12, 7), (11, 7), (10, 7)]
        for (r, c) in enemy_trail:
            self.grid[r][c] = -2

        # Agent
        self.agent_pos = [2, 2]
        self.in_territory = True
        self.agent_territory = [(1,1),(1,2),(2,1),(2,2),(3,1),(3,2),(4,1),(4,2),(2,3)]
        self.agent_trail = []
        for r, c in self.agent_territory:
            self.grid[r][c] = 1

        # return obs, {}
        return self._get_obs(), {}
    
    def step(self, action):
        action = int(action)
        self.steps += 1

        reward = -0.015
        terminated = False
        truncated = False

        directions = {
            0: (-1, 0),
            1: (0, 1),
            2: (1, 0),
            3: (0, -1)
        }

        dr, dc = directions[action]
        nr = self.agent_pos[0] + dr
        nc = self.agent_pos[1] + dc
        # ----------------------------
        # Compute next position
        # ----------------------------

        if nr < 0 or nr >= self.grid_size or nc < 0 or nc >= self.grid_size:
            reward = -2.5
            terminated = True
            return self._get_obs(), reward, terminated, truncated, {}

        cell = self.grid[nr][nc]

        # ----------------------------
        # Death checks
        # ----------------------------

        # Hit own trail
        if cell == -1:
            reward = -2.5
            terminated = True
            return self._get_obs(), reward, terminated, truncated, {}

        # Kill enemy
        if cell == -2:
            self.grid[self.grid == 2] = 0
            self.grid[self.grid == -2] = 0

            self.agent_pos = [nr, nc]

            reward = 7
            terminated = True
            return self._get_obs(), reward, terminated, truncated, {}

        # ----------------------------
        # Move agent
        # ----------------------------

        # Outside territory -> continue trail
        if not self.in_territory and cell != 1:
            self.grid[self.agent_pos[0]][self.agent_pos[1]] = -1
            self.agent_trail.append(tuple(self.agent_pos))
            self.agent_pos = [nr, nc]
            if cell == 0:
                reward = -0.005
            else:           # enemy territory
                reward = -0.02

        # Moving inside territory
        elif self.in_territory and cell == 1:
            self.agent_pos = [nr, nc]
            reward = -0.05

        # Leaving territory
        elif self.in_territory and cell != 1:
            self.in_territory = False
            self.agent_pos = [nr, nc]
            if cell == 0:
                reward = -0.005
            else:
                reward = -0.02

        # Returning to territory
        else:
            self.grid[self.agent_pos[0]][self.agent_pos[1]] = -1
            self.agent_trail.append(tuple(self.agent_pos))

            old_area = len(self.agent_territory)
            enemy_before = np.sum(self.grid == 2)

            self.capture()

            new_area = len(self.agent_territory)
            enemy_after = np.sum(self.grid == 2)

            captured_cells = new_area - old_area
            enemy_captured = enemy_before - enemy_after

            reward = 0.5 * captured_cells + 2.0 * enemy_captured

            self.agent_pos = [nr, nc]
            self.in_territory = True

        if self.steps >= self.max_steps:
            truncated = True

        return self._get_obs(), reward, terminated, truncated, {}

    def _get_obs(self):
        obs = np.zeros((self.grid_size, self.grid_size, 4), dtype=np.float32)
        # Your territory
        obs[:, :, 0] = (self.grid == 1)
        # Enemy territory
        obs[:, :, 1] = (self.grid == 2)
        # Enemy trail
        obs[:, :, 2] = (self.grid == -2).astype(np.float32)
        # Your trail
        obs[:, :, 3] = (self.grid == -1).astype(np.float32)
        # Agent head
        r, c = self.agent_pos
        obs[r, c, 3] = 0.5
        return obs  # shape (grid_size, grid_size, 4)
    
    def capture(self):
        # Convert trail to territory
        for r, c in self.agent_trail:
            self.grid[r][c] = 1
        helper_grid = self.grid.copy()
        # DFS from all boundary cells
        for row in range(self.grid_size):
            self.dfs(helper_grid, row, 0)
            self.dfs(helper_grid, row, self.grid_size - 1)
        for col in range(self.grid_size):
            self.dfs(helper_grid, 0, col)
            self.dfs(helper_grid, self.grid_size - 1, col)
        # Capture enclosed region
        self.agent_territory = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if helper_grid[row][col] != 1:
                    self.grid[row][col] = 1
                if self.grid[row][col] == 1:
                    self.agent_territory.append((row, col))
        # Clear trail
        self.agent_trail = []

    def dfs(self, helper_grid, row, col):
        if(row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size): return
        cell = self.grid[row][col]
        if (helper_grid[row][col] == 1 or cell == -1): return

        helper_grid[row][col] = 1

        self.dfs(helper_grid, row + 1, col)
        self.dfs(helper_grid, row - 1, col)
        self.dfs(helper_grid, row, col + 1)
        self.dfs(helper_grid, row, col - 1)