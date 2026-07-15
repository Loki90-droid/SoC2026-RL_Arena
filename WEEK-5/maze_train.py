import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
import pygame


class MazeEnv(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(4)
        """
        - Using np.int8 for observations can cause training instability. Neural networks expect float inputs. Try np.float32 and normalize values to [0, 1] instead of raw 0-3.
        - Add a max_steps parameter to prevent episodes from running forever.
        """
        # self.observation_space = spaces.Box(0, 3, (1, 10, 10), dtype=np.int8)
        self.observation_space = spaces.Box(0, 1, (1, 10, 10), dtype=np.float32)
        # TODO
        self._max_steps = 200
        self._steps = 0
        self._maze = np.array([
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,0,1],
        [1,0,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,1,0,1],
        [1,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,1,0,0,1,0,1],
        [1,0,1,0,0,0,1,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
        ])
        self.visited = np.zeros((10,10), dtype=np.int8)
        self.start_pos = (1, 1)
        self.goal_pos = (8, 8)
        self.agent_pos = self.start_pos
        return

    def _get_obs(self):
        """
        Note: Normalize values to [0, 1] so the neural network sees well-scaled inputs. Raw int values 0-3 can produce large gradients and slow or unstable learning.
        """
        obs = self._maze.copy()
        obs[self.goal_pos] = 2
        obs[self.agent_pos] = 3
        obs = obs.astype(np.float32)
        obs /= 3.0
        return obs.reshape(1,10,10)

    def reset(self, seed=None, options=None):
        # Track step count here so you can truncate long episodes in step().
        self._steps = 0
        self.agent_pos = self.start_pos
        self.visited.fill(0)
        self.visited[self.start_pos] = 1
        return self._get_obs(), {}

    def step(self, action):
        """
        Note: Add a truncation condition (e.g., max 200 steps) — the episode should end if the agent hasn't reached the goal in time.
        Experiment with different reward values!!
         - wall penalty (-0.5), step penalty (-0.01), revisit penalty (-0.3)
         - What happens if you increase the goal reward? (+1 is quite small)
         - Try removing the revisit penalty and see what the agent does
        """
        if action == 0:
            dr, dc = -1, 0
        elif action == 1:
            dr, dc = 0, 1
        elif action == 2:
            dr, dc = 1, 0
        else:
            dr, dc = 0, -1
        reward = 0
        if self._maze[self.agent_pos[0]+dr][self.agent_pos[1]+dc]==0:
            self.agent_pos = (self.agent_pos[0] + dr, self.agent_pos[1] + dc)
            if self.agent_pos==self.goal_pos: reward = 10
            elif self.visited[self.agent_pos] == 1: reward = -0.3
            else: reward = -0.01
        else :
            reward = -0.5
        self._steps += 1
        self.visited[self.agent_pos] = 1
        return self._get_obs(), reward, self.agent_pos == self.goal_pos, self._steps>=self._max_steps, {}
        

    def _render_rgb(self):
        # Note: Return shape (height, width, 3) with uint8 values 0-255.
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        for i in range(10):
            for j in range(10):
                if self._maze[i][j] == 0:
                    img[i][j] = (255, 255, 255)
        img[self.goal_pos] = (0, 255, 0)
        img[self.agent_pos] = (255, 0, 0)
        return img


def main():
    env = MazeEnv()
    """
    - PPO's default ent_coef=0 means NO exploration pressure. If your agent gets stuck at the start, try ent_coef=0.01 to encourage trying things.
    - Try different learning rates (lr=0.0003 is the default):
      - too high -> unstable training
      - too low  -> slow progress
    - Increase total_timesteps if the agent hasn't converged.
    """
    model = PPO("MlpPolicy", env, verbose=1, n_steps=1024, batch_size=64, ent_coef=0.01)
    model.learn(total_timesteps=50_000)
    model.save("maze_ppo")


if __name__ == "__main__":
    main()
