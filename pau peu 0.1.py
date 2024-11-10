
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

# Load the background image
background = pygame.image.load('background.png')

# Player attributes
player_pos = [WIDTH // 2, HEIGHT // 2]
player_angle = 0
player_health = 100
player_shield = 0  # Player shield amount

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font for displaying the kill counter
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Bullets and enemies
bullets = []
enemies = []
enemy_bullets = []

# Kill counter
kill_count = 0

# Shield drop
shield_drops = []

# Enemy spawn function
def spawn_enemy():
    enemy_pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
    enemies.append(enemy_pos)

# Draw functions
def draw_bullet(screen, bullet):
    pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 5)

def draw_enemy_bullet(screen, bullet):
    pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[1])), 5)

def draw_enemy(screen, enemy):
    pygame.draw.circle(screen, RED, enemy, 20)

def draw_shield_drop(screen, drop_pos):
    pygame.draw.circle(screen, BLUE, drop_pos, 15)

# Collision detection functions
def check_collision(bullets, enemies):
    for bullet in bullets:
        for enemy in enemies:
            if math.hypot(bullet[0] - enemy[0], bullet[1] - enemy[1]) < 20:
                return bullet, enemy
    return None, None

def check_player_collision(player_pos, enemies):
    for enemy in enemies:
        if math.hypot(player_pos[0] - enemy[0], player_pos[1] - enemy[1]) < 20:
            return enemy
    return None

def check_player_bullet_collision(player_pos, enemy_bullets):
    for bullet in enemy_bullets:
        if math.hypot(player_pos[0] - bullet[0], player_pos[1] - bullet[1]) < 10:
            return bullet
    return None

def check_player_shield_pickup(player_pos, shield_drops):
    for drop in shield_drops:
        if math.hypot(player_pos[0] - drop[0], player_pos[1] - drop[1]) < 20:
            return drop
    return None

# Draw health and shield bar
def draw_health_and_shield_bar(screen, health, shield):
    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, 2 * health, 20))
    # Draw shield bar
    pygame.draw.rect(screen, BLUE, (10, 40, 200, 20))
    pygame.draw.rect(screen, WHITE, (10, 40, 2 * shield, 20))

# Draw kill counter
def draw_kill_counter(screen, kills):
    text = font.render(f'Kills: {kills}', True, WHITE)
    screen.blit(text, (WIDTH - 150, 10))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bullet_speed = 10
                bullet_dx = math.cos(math.radians(player_angle)) * bullet_speed
                bullet_dy = -math.sin(math.radians(player_angle)) * bullet_speed
                bullets.append([player_pos[0], player_pos[1], bullet_dx, bullet_dy])

    # Draw the background image
    screen.blit(background, (0, 0))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        player_pos[1] -= 5
    if keys[K_s]:
        player_pos[1] += 5
    if keys[K_a]:
        player_pos[0] -= 5
    if keys[K_d]:
        player_pos[0] += 5

    # Rotate player
    if keys[K_LEFT]:
        player_angle += 5
    if keys[K_RIGHT]:
        player_angle -= 5

    # Draw player
    pygame.draw.circle(screen, WHITE, player_pos, 20)
    pygame.draw.line(screen, WHITE, player_pos, 
                     (player_pos[0] + 50 * math.cos(math.radians(player_angle)), 
                      player_pos[1] - 50 * math.sin(math.radians(player_angle))), 2)

    # Update and draw bullets
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        draw_bullet(screen, bullet)

    # Remove off-screen bullets
    bullets = [bullet for bullet in bullets if 0 <= bullet[0] <= WIDTH and 0 <= bullet[1] <= HEIGHT]

    # Update and draw enemies
    for enemy in enemies:
        if enemy[0] < player_pos[0]:
            enemy[0] += 1
        if enemy[0] > player_pos[0]:
            enemy[0] -= 1
        if enemy[1] < player_pos[1]:
            enemy[1] += 1
        if enemy[1] > player_pos[1]:
            enemy[1] -= 1
        draw_enemy(screen, enemy)
        if random.randint(1, 100) < 2:
            bullet_speed = 5
            angle_to_player = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])
            bullet_dx = math.cos(angle_to_player) * bullet_speed
            bullet_dy = math.sin(angle_to_player) * bullet_speed
            enemy_bullets.append([enemy[0], enemy[1], bullet_dx, bullet_dy])

    # Update and draw enemy bullets
    for bullet in enemy_bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        draw_enemy_bullet(screen, bullet)

    # Remove off-screen enemy bullets
    enemy_bullets = [bullet for bullet in enemy_bullets if 0 <= bullet[0] <= WIDTH and 0 <= bullet[1] <= HEIGHT]

    # Check for collisions
    bullet_hit, enemy_hit = check_collision(bullets, enemies)
    if bullet_hit and enemy_hit:
        bullets.remove(bullet_hit)
        enemies.remove(enemy_hit)
        kill_count += 1  # Increment kill counter

        # Every 10 kills, drop a shield with 100% probability
        if kill_count % 10 == 0:
            shield_drops.append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])

    player_hit = check_player_collision(player_pos, enemies)
    if player_hit:
        enemies.remove(player_hit)
        if player_shield > 0:
            player_shield -= 10
            if player_shield < 0:
                player_health += player_shield  # Adjust health if shield goes negative
                player_shield = 0
        else:
            player_health -= 10
        if player_health <= 0:
            running = False

    enemy_bullet_hit = check_player_bullet_collision(player_pos, enemy_bullets)
    if enemy_bullet_hit:
        enemy_bullets.remove(enemy_bullet_hit)
        if player_shield > 0:
            player_shield -= 10
            if player_shield < 0:
                player_health += player_shield  # Adjust health if shield goes negative
                player_shield = 0
        else:
            player_health -= 10
        if player_health <= 0:
            running = False

    # Check for shield pickup
    shield_pickup = check_player_shield_pickup(player_pos, shield_drops)
    if shield_pickup:
        shield_drops.remove(shield_pickup)
        player_shield = min(player_shield + 25, 100)  # Add 25 shield, max 100

    # Update and draw shield drops
    for drop in shield_drops:
        draw_shield_drop(screen, drop)

    # Spawn new enemies
    if random.randint(1, 100) < 2:
        spawn_enemy()

    # Draw health and shield bar
    draw_health_and_shield_bar(screen, player_health, player_shield)

    # Draw kill counter
    draw_kill_counter(screen, kill_count)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
