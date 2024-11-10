import pygame
from pygame.locals import *
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('peu peu')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Font for displaying the kill counter and game over screen
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Load the background image
background = pygame.image.load('background.png')

# Load sounds (if applicable)
# pygame.mixer.init()
# bullet_sound = pygame.mixer.Sound('bullet.wav')
# hit_sound = pygame.mixer.Sound('hit.wav')

# Clock
clock = pygame.time.Clock()

# Player attributes
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5  # Player movement speed
player_health = 100
player_shield = 0  # Player shield amount

# Bullets and enemies
bullets = []
enemies = []

# Kill counter
kill_count = 0

# Draw functions
def draw_bullet(screen, bullet):
    pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 5)

def draw_enemy(screen, enemy):
    pygame.draw.circle(screen, RED, enemy, 20)

# Draw player as a circle
def draw_player(screen, player_pos):
    pygame.draw.circle(screen, GREEN, (int(player_pos[0]), int(player_pos[1])), 15)

# Collision detection functions
def check_collision(bullets, enemies):
    for bullet in bullets:
        for enemy in enemies:
            if math.hypot(bullet[0] - enemy[0], bullet[1] - enemy[1]) < 20:
                return bullet, enemy
    return None, None

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    # Player movement with WASD
    if keys[K_w]:
        player_pos[1] -= player_speed
    if keys[K_s]:
        player_pos[1] += player_speed
    if keys[K_a]:
        player_pos[0] -= player_speed
    if keys[K_d]:
        player_pos[0] += player_speed

    # Shooting mechanics
    if keys[K_SPACE]:
        bullet_pos = [player_pos[0], player_pos[1] - 20]
        bullets.append([bullet_pos[0], bullet_pos[1]])
        # Uncomment below if sound is loaded
        # bullet_sound.play()

    # Update bullet positions
    for bullet in bullets[:]:
        bullet[1] -= 10  # Bullets move upwards
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Enemy spawn and movement
    if random.randint(0, 100) < 2:  # Small chance to spawn an enemy
        enemy_pos = [random.randint(0, WIDTH), 0]
        enemies.append(enemy_pos)

    for enemy in enemies[:]:
        enemy[1] += 2  # Enemies move downwards
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

    # Check collisions
    bullet, enemy = check_collision(bullets, enemies)
    if bullet and enemy:
        bullets.remove(bullet)
        enemies.remove(enemy)
        kill_count += 1
        # Uncomment below if sound is loaded
        # hit_sound.play()

    # Drawing
    screen.fill(BLACK)  # Fill screen with black before drawing the background
    screen.blit(background, (0, 0))  # Draw the background image
    draw_player(screen, player_pos)
    for bullet in bullets:
        draw_bullet(screen, bullet)
    for enemy in enemies:
        draw_enemy(screen, enemy)

    # Kill counter
    kill_text = font.render(f'Kills: {kill_count}', True, WHITE)
    screen.blit(kill_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()