import gymnasium as gym
from stable_baselines3 import PPO

env = gym.make("CartPole-v1", render_mode="human")
model = PPO("MlpPolicy", env).learn(50_000)

obs, _ = env.reset()
for _ in range(2000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    env.render()
    if terminated or truncated:
        obs, _ = env.reset()
env.close()
