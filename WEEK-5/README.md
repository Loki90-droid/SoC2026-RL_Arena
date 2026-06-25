# Week 4 — RL Environment Design & Training

This week you will learn how to build your own reinforcement learning environment and train an agent to solve it.

## Resources

- [Official Gymnasium Documentation](https://gymnasium.farama.org/introduction/create_custom_env/)
- [Video Tutorial](https://www.youtube.com/watch?v=bD6V3rcr_54)
- [Example Environment Implementation](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)

## Task 1 — CartPole (Warmup)

Run this file to see a pre-built environment in action:

```
python3 cartpole.py
```

Read the code. It creates a CartPole environment from Gymnasium, trains a PPO agent on it, and then lets the trained agent balance the pole. Learn more about cartpole from [here](https://gymnasium.farama.org/environments/classic_control/cart_pole/)


## Task 2 — Maze

You need to train an agent to navigate from the start to the goal in a maze. The maze has walls (1)and paths (0). The agent can move up, right, down, or left.

Example Maze layout:
```
1 1 1 1 1 1 1 1 1 1
1 0 0 0 1 0 0 0 0 1
1 0 1 0 1 0 1 1 0 1
1 0 1 0 0 0 0 0 0 1
1 0 1 1 1 1 1 1 0 1
1 0 0 0 0 0 0 1 0 1
1 1 1 0 1 1 0 1 0 1
1 0 0 0 1 0 0 1 0 1
1 0 1 0 0 0 1 0 0 1
1 1 1 1 1 1 1 1 1 1
```
Start is at (1,1) and end at (8,8)
You need to complete the MazeEnv class in `maze_train.py`.

### Function Specifics

`__init__`
It stores the action space, observation space, maze layout, the start position, and the goal position.
- `self.action_space = spaces.Discrete(4)` means the agent has 4 choices: up, right, down, and left.
- `self.observation_space = Box(0, 3, (1, 10, 10), np.int8)` means the observation is a 10 by 10 grid where each cell has a value between 0 and 3. The (1, 10, 10) shape means there is one channel (like a black-and-white image) with 10 rows and 10 columns. You may want to use float32 and a normalized cell value for better results.

`_get_obs(self)`
This function turns the current maze and agent position into a numpy array.
The returned array should have shape `(1, 10, 10)` and use these values:
- `0` for empty path cells
- `1` for wall cells
- `2` for the goal cell
- `3` for the agent's current position
- Normalize them to [0,1]. 
  
`reset(self, seed=None)`
This function is called every time a new episode starts. It puts the agent back at the start position.
Read the documentation once for more detailed information.

`step(self, action)`
This function updates the agent's position based on the chosen action. It should check whether the move is valid, apply rewards, and determine if the goal has been reached. A positive reward is given for reaching the goal, while small penalties encourage the agent to avoid invalid moves and find efficient paths. The function then returns the outcome of the action.

`_render_rgb(self)`
This function creates a colour representation of the maze using a NumPy array. This array is used to render the maze using the blit function. Make sure to check its use case in maze.py

### Do this after you are done:

Install dependencies:
```
pip install -r requirements.txt
```

First, train the agent:
```
python3 maze_train.py
```

Then watch it solve the maze:
```
python3 maze.py
```
