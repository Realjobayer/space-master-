import pygame
from pygame.locals import *
import math
import random

#something
pygame.init()

# Screen 
WIDTH, HEIGHT = 1320, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('peu peu')
#background

# Player attributes
player_pos = [WIDTH // 2, HEIGHT // 2]
player_angle = 0
player_health = 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()

# Bullet ..
bullets = []

# Enemy ..
enemies = []
enemy_bullets = []

# enemies
def spawn_enemy():
    enemy_pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
    enemies.append(enemy_pos)

# Draw bullet
def draw_bullet(screen, bullet):
    pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 5)

# Draw enemy bullet
def draw_enemy_bullet(screen, bullet):
    pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[1])), 5)

# Draw enemy
def draw_enemy(screen, enemy):
    pygame.draw.circle(screen, RED, enemy, 20)

# bullets and enemies
def check_collision(bullets, enemies):
    for bullet in bullets:
        for enemy in enemies:
            if math.hypot(bullet[0] - enemy[0], bullet[1] - enemy[1]) < 20:
                return bullet, enemy
    return None, None

# player and enemies
def check_player_collision(player_pos, enemies):
    for enemy in enemies:
        if math.hypot(player_pos[0] - enemy[0], player_pos[1] - enemy[1]) < 20:
            return enemy
    return None

#player and enemy bullets
def check_player_bullet_collision(player_pos, enemy_bullets):
    for bullet in enemy_bullets:
        if math.hypot(player_pos[0] - bullet[0], player_pos[1] - bullet[1]) < 10:
            return bullet
    return None

# Draw health bar
def draw_health_bar(screen, health):
    pygame.draw.rect(screen, RED, (10, 10, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, 2 * health, 20))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Fire bullet
                bullet_speed = 10
                bullet_dx = math.cos(math.radians(player_angle)) * bullet_speed
                bullet_dy = -math.sin(math.radians(player_angle)) * bullet_speed
                bullets.append([player_pos[0], player_pos[1], bullet_dx, bullet_dy])

    # Clear the screen
    screen.fill(BLACK)

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

    # Update bullets
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        draw_bullet(screen, bullet)

    # Remove bullets that are off-screen
    bullets = [bullet for bullet in bullets if 0 <= bullet[0] <= WIDTH and 0 <= bullet[1] <= HEIGHT]

    # Update enemies
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
        # Enemy shooting
        if random.randint(1, 100) < 2:
            bullet_speed = 5
            angle_to_player = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])
            bullet_dx = math.cos(angle_to_player) * bullet_speed
            bullet_dy = math.sin(angle_to_player) * bullet_speed
            enemy_bullets.append([enemy[0], enemy[1], bullet_dx, bullet_dy])

    # Update enemy bullets
    for bullet in enemy_bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        draw_enemy_bullet(screen, bullet)

    # Remove enemy bullets that are off-screen
    enemy_bullets = [bullet for bullet in enemy_bullets if 0 <= bullet[0] <= WIDTH and 0 <= bullet[1] <= HEIGHT]

    # Check for collisions between bullets and enemies
    bullet_hit, enemy_hit = check_collision(bullets, enemies)
    if bullet_hit and enemy_hit:
        bullets.remove(bullet_hit)
        enemies.remove(enemy_hit)

    # Check for collisions between player and enemies
    player_hit = check_player_collision(player_pos, enemies)
    if player_hit:
        enemies.remove(player_hit)
        player_health -= 10
        if player_health <= 0:
            running = False

    # Check for collisions between player and enemy bullets
    enemy_bullet_hit = check_player_bullet_collision(player_pos, enemy_bullets)
    if enemy_bullet_hit:
        enemy_bullets.remove(enemy_bullet_hit)
        player_health -= 10
        if player_health <= 0:
            running = False

    # Spawn new enemies
    if random.randint(1, 100) < 2:
        spawn_enemy()

    # Draw health bar
    draw_health_bar(screen, player_health)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
