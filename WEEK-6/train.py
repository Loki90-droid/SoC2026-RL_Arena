from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from gym_env import RL_Arena_Env

env = RL_Arena_Env(grid_size=15)
#check_env(env)
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100_000)
model.save("paper_io_agent")