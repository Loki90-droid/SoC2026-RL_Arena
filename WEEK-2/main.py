import pygame
from constants import *
from player import Player
from game import Game
from renderer import *
score_1= 0
score_2= 0
pygame.init()
font = pygame.font.Font(None, 48)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RL Arena")
clock = pygame.time.Clock()

player1 = Player(5, 5, RED)
player2 = Player(15, 15, BLUE)

game = Game(ROWS, COLS)
game.add_player(player1)
game.add_player(player2)

actions_wasd = {pygame.K_w: (0, -1), pygame.K_a: (-1, 0),
                pygame.K_s: (0, 1), pygame.K_d: (1, 0)}
actions_arrows = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
                  pygame.K_RIGHT: (1, 0), pygame.K_LEFT: (-1, 0)}

running = True
game_over = False

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.reset()
                score_1 = 0
                score_2 = 0
                game_over = False
            if event.key in actions_wasd:
                player1.dir = actions_wasd[event.key]
            if event.key in actions_arrows:
                player2.dir = actions_arrows[event.key]
    if not game_over:
        game.update()
        score_1+=int(player1.alive)
        score_2+=int(player2.alive)
        if not player1.alive or not player2.alive:
            game_over = True
    draw_grid(screen,game)
    score_text = font.render(f"Score 1: {score_1}  Score 2: {score_2}", True, GREEN)
    screen.blit(score_text, (10,10))
    for player in game.players:
        if player.alive:
            draw_player(screen,player)
    if game_over:
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        
    # Handle quit event
    # Read keyboard, update player directions
    # Call game.update()
    # If anyone died, change game_over var
    
    # Draw everything
    # If game over, render text on top
    pygame.display.update()
