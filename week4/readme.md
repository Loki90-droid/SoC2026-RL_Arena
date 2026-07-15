# Week 4 – RL Training

This week I learnt the basics of RL and learnt how an agent interacts with an environment by taking actions and receiving rewards.

## What I Learnt

### RL Basics

- An RL problem consists of an {agent},{environment},{states},{actions},and {rewards}.
- The objective of the agent is to learn a strategy that maximizes the total reward.

### Understanding Gymnasium Environments

Learnt how a custom environment is built using Gymnasium and the functions like:

- `__init__()` , `reset()` , `step(action)` , `render()`

### Action Space and Observation Space

- how an environment defines the set of actions available to an agent.
- how the current state of the environment is shown as observations given to the model.

### State Representation

In the maze environment:

- `0` represents an empty path.
- `1` represents a wall.
- `2` represents the goal.
- `3` represents the current position of the agent.

- observations are often normalized before being given to a neural network.

### Reward System

how rewards influence the RL agent.

- Positive reward for reaching the goal.
- Penalties for invalid moves or unnecessary actions.
- Small changes in rewards can lead to very different behaviours.

### Episode Completion

environments need termination conditions such as:

- Reaching the goal.
- Exceeding a maximum number of steps.

### PPO (Proximal Policy Optimization)

Got introduced to PPO using Stable-Baselines3 and understood the general workflow:

1. Create an environment.
2. Train the agent.
3. Save the model.
4. Load the trained model and evaluate it.

### CartPole Environment

Explored the CartPole environment and observed how a PPO agent learns to balance the pole.

### Custom Maze Environment

Built and trained an agent to navigate through a maze by:

- Defining states and actions.
- Designing rewards.
- Training the agent using PPO.
- Visulizing using pygame
