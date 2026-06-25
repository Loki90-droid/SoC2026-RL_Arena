import pygame
from maze_train import MazeEnv
from stable_baselines3 import PPO


def main():
    env = MazeEnv()
    model = PPO.load("maze_ppo")

    obs, _ = env.reset()
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(int(action))
            done = terminated or truncated

        rgb = env._render_rgb()
        surf = pygame.surfarray.make_surface(rgb.transpose(1, 0, 2))
        screen.blit(pygame.transform.scale(surf, (500, 500)), (0, 0))
        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
