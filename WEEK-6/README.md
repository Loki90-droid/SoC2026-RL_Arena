# Week 6

Turn your Paper.io game into a Gym environment so an RL agent can play it.

## What changed

No second player. The grid starts with a static enemy territory and trails.

- **Enemy territory** — blocks the player
- **Enemy trail** — touch it and the enemy dies.
- **Own trail** — touch it and the player dies.

The agent wins if:
- It has more territory than the enemy when time runs out, **or**
- It kills the enemy by touching its trail.

## Grid encoding (same as Week 3)

```
0   = empty
+N  = player N's territory
-N  = player N's trail
```

You are +1/-1. Enemy is +2/-2.


## Building the wrapper

Create `gym_env.py`:

```python
import gymnasium as gym
import numpy as np

class RL_Arena_Env(gym.Env):

    def __init__(self, grid_size=15):
        super().__init__()
        self.grid_size = grid_size
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(grid_size, grid_size, 3), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(4)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # place enemy territory + trail, spawn agent
        # return obs, {}

    def step(self, action):
        # 1. move agent
        # 2. place trail, check capture
        # 3. check enemy trail → kill enemy
        # 4. compute reward
        # 5. check dead
        # return obs, reward, terminated, truncated, {}

    def render(self):
        pass

    def _get_obs(self):
        return obs  # shape (grid_size, grid_size, 3)
```

## Observation

```
Channel 0 — your territory        1.0 or 0.0
Channel 1 — enemy territory       1.0 or 0.0
Channel 2 — enemy trail + head    0.5 = your head, 1.0 = enemy trail
```

The agent needs to see the difference between enemy territory (blocks) and enemy trail (killable).

Keep grid **15x15 max**.

### Grid vs Observation

**Grid** is your game logic — numbers like 0, +1, -1, +2, -2.

**Observation** is what the agent sees — 3 channels, each with 1.0 or 0.0.

`_get_obs()` converts one to the other:

```
grid[r][c] == +1  →  channel 0[r][c] = 1.0   (your territory)
grid[r][c] == +2  →  channel 1[r][c] = 1.0   (enemy territory)
grid[r][c] == -2  →  channel 2[r][c] = 1.0   (enemy trail)
```

## Setting up the enemy in `reset()`

```python
def reset(self, seed=None, options=None):
    super().reset(seed=seed)

    self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)

    enemy_territory = [(10,10), (10,11), (10,12),
                       (11,10), (11,11), (11,12),
                       (12,10), (12,11), (12,12)]
    for (r, c) in enemy_territory:
        self.grid[r][c] = 2

    enemy_trail = [(7,5), (7,6), (7,7), (7,8), (7,9)]
    for (r, c) in enemy_trail:
        self.grid[r][c] = -2

    self.agent_pos = [1, 1]
    self.agent_territory = [(1,1), (1,2), (2,1)]

    return self._get_obs(), {}
```

Enemy never moves. Touch its trail = enemy dies. Then its territory is free.

**Randomize enemy position** across episodes so the agent doesn't memorize a path.

## Reward design
 > Reward tuning takes time. Don't rush it : try something, watch what the agent does, then change it.

- Every step outside your territory leaves a trail. Should the agent care how long it stays out?
- A 50-pixel capture and a 2-pixel capture shouldn't feel the same.
- Killing the enemy changes everything — that should be the biggest reward.
- The agent needs to **beat** the enemy's territory, not just grow its own. Capturing 10 tiles doesn't help if the enemy still has 20.

After the enemy dies, the agent wins.

## Training

```python
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from gym_env import RL_Arena_Env

env = RL_Arena_Env(grid_size=15)
check_env(env)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=300_000)
model.save("paper_io_agent")
```


## If stuck

**Agent just stands still** — reward for just staying alive is too high. Lower it.

**Training is slow** — try 10x10 grid and 100k timesteps for testing.

**Agent dies every episode** — check reset() gives room. Agent probably hits its own trail.
