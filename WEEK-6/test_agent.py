from stable_baselines3 import PPO
from gym_env import RL_Arena_Env
import pygame

env = RL_Arena_Env()
model = PPO.load("paper_io_agent")
obs, _ = env.reset()

pygame.init()
pygame.display.set_caption("Paper.io RL Environment")
cell_size = 40
window = pygame.display.set_mode((env.grid_size * cell_size, env.grid_size * cell_size))
clock = pygame.time.Clock()

def render(env):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    window.fill((255, 255, 255))
    print(env.grid[9][11])
    print(env.grid[1][3])
    for r in range(env.grid_size):
        for c in range(env.grid_size):
            value = env.grid[r][c]
            if value == 1:
                color = (0, 120, 255)
            elif value == -1:
                color = (0, 180, 255)
            elif value == 2:
                color = (255, 140, 0)
            elif value == -2:
                color = (255, 80, 80)
            else:
                color = (245, 245, 245)
            pygame.draw.rect( window, color, (c * cell_size, r * cell_size, cell_size, cell_size))
            pygame.draw.rect(window, (180, 180, 180), (c * cell_size, r * cell_size, cell_size, cell_size), 1)
    # Draw player head
    pygame.draw.circle(window, (0, 255, 0), (env.agent_pos[1] * cell_size + cell_size // 2, env.agent_pos[0] * cell_size + cell_size // 2), cell_size // 3)
    #Score
    font = pygame.font.SysFont(None, 24)

    player = int((env.grid == 1).sum())
    enemy = int((env.grid == 2).sum())

    text = font.render(
        f"P:{player}  E:{enemy}",
        True,
        (0,0,0)
    )

    window.blit(text, (8,8))
    pygame.display.flip()
    clock.tick(1)

while True:
    action, _ = model.predict(
        obs,
        deterministic=True
    )
    obs, reward, terminated, truncated, _ = env.step(action)
    render(env)
    if terminated or truncated:
        obs, _ = env.reset()