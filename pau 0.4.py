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

# Clock
clock = pygame.time.Clock()

# Player attributes
player_pos = [WIDTH // 2, HEIGHT // 2]
player_angle = 0
player_health = 100
player_shield = 0  # Player shield amount

# Bullets, enemies, and boss
bullets = []
enemies = []
enemy_bullets = []
boss = None  # Boss doesn't exist at the start

# Kill counter
kill_count = 0

# Shield drop
shield_drops = []

# Boss attributes
boss_health = 300
boss_pos = [WIDTH // 2, HEIGHT // 4]  # Boss starts near the top center
boss_alive = False  # Boss isn't spawned yet

def reset_game():
    global player_pos, player_angle, player_health, player_shield
    global bullets, enemies, enemy_bullets, boss, kill_count, shield_drops, boss_health, boss_pos, boss_alive

    # Reset all game attributes
    player_pos = [WIDTH // 2, HEIGHT // 2]
    player_angle = 0
    player_health = 100
    player_shield = 0

    bullets = []
    enemies = []
    enemy_bullets = []
    boss = None

    kill_count = 0
    shield_drops = []

    boss_health = 300
    boss_pos = [WIDTH // 2, HEIGHT // 4]
    boss_alive = False

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

def draw_boss(screen, boss_pos):
    pygame.draw.circle(screen, YELLOW, boss_pos, 50)  # Larger circle for the boss

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

def check_boss_collision(bullets, boss_pos):
    for bullet in bullets:
        if math.hypot(bullet[0] - boss_pos[0], bullet[1] - boss_pos[1]) < 50:
            return bullet
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

# Draw boss health bar
def draw_boss_health_bar(screen, boss_health):
    # Draw boss health bar if the boss is alive
    if boss_health > 0:
        pygame.draw.rect(screen, RED, (WIDTH - 250, 50, 200, 20))
        pygame.draw.rect(screen, GREEN, (WIDTH - 250, 50, int(200 * (boss_health / 300)), 20))

# Game over screen
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = game_over_font.render('GAME OVER', True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    
    sub_text = font.render('Press Enter to restart', True, WHITE)
    screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 50))
    
    pygame.display.flip()

    # Wait for player input to restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # If Enter key is pressed
                    reset_game()
                    waiting = False

# Main game loop
while True:  # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
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

        # Rotate player to face the mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_angle = math.degrees(math.atan2(player_pos[1] - mouse_y, mouse_x - player_pos[0]))

        # Gun oscillation effect
        gun_offset = 5 * math.sin(math.radians(player_angle * 4))  # Adjust frequency as needed

        # Draw player
        pygame.draw.circle(screen, WHITE, player_pos, 20)
        pygame.draw.line(screen, WHITE, player_pos, 
                         (player_pos[0] + 50 * math.cos(math.radians(player_angle)), 
                          player_pos[1] - 50 * math.sin(math.radians(player_angle)) + gun_offset), 2)

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

        # Check for bullet-enemy collisions
        bullet, enemy = check_collision(bullets, enemies)
        if bullet and enemy:
            bullets.remove(bullet)
            enemies.remove(enemy)
            kill_count += 1  # Increment kill count
            # Randomly drop shield with a small probability
            if random.random() < 0.05:
                shield_drops.append(enemy[:])  # Drop at enemy's position

        # Check for player-enemy collisions
        enemy = check_player_collision(player_pos, enemies)
        if enemy:
            if player_shield > 0:
                player_shield -= 10  # Reduce shield instead of health
            else:
                player_health -= 10  # Reduce health if no shield
            enemies.remove(enemy)
            if player_health <= 0:
                running = False  # End the game

        # Spawn an enemy every 100 frames (adjust as needed)
        if pygame.time.get_ticks() % 100 == 0:
            spawn_enemy()

        # Draw shield drops and check for pickup
        for drop in shield_drops:
            draw_shield_drop(screen, drop)
        drop = check_player_shield_pickup(player_pos, shield_drops)
        if drop:
            player_shield = min(player_shield + 20, 100)  # Increase shield, up to max 100
            shield_drops.remove(drop)

        # Update and draw enemy bullets
        for bullet in enemy_bullets:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            draw_enemy_bullet(screen, bullet)

        # Check for player-enemy bullet collisions
        bullet = check_player_bullet_collision(player_pos, enemy_bullets)
        if bullet:
            if player_shield > 0:
                player_shield -= 10  # Reduce shield instead of health
            else:
                player_health -= 10  # Reduce health if no shield
            enemy_bullets.remove(bullet)
            if player_health <= 0:
                running = False  # End the game

        # Spawn the boss after 10 kills
        if kill_count >= 10 and not boss_alive:
            boss_alive = True
            boss_pos = [WIDTH // 2, HEIGHT // 4]  # Position the boss near the top center

        # Update and draw the boss if it's alive
        if boss_alive:
            draw_boss(screen, boss_pos)

            # Boss movement
            if boss_pos[0] < player_pos[0]:
                boss_pos[0] += 1
            if boss_pos[0] > player_pos[0]:
                boss_pos[0] -= 1
            if boss_pos[1] < player_pos[1]:
                boss_pos[1] += 1
            if boss_pos[1] > player_pos[1]:
                boss_pos[1] -= 1

            # Boss fires a bullet every 50 frames (adjust as needed)
            if pygame.time.get_ticks() % 50 == 0:
                bullet_speed = 5
                bullet_dx = (player_pos[0] - boss_pos[0]) / math.hypot(player_pos[0] - boss_pos[0], player_pos[1] - boss_pos[1]) * bullet_speed
                bullet_dy = (player_pos[1] - boss_pos[1]) / math.hypot(player_pos[0] - boss_pos[0], player_pos[1] - boss_pos[1]) * bullet_speed
                enemy_bullets.append([boss_pos[0], boss_pos[1], bullet_dx, bullet_dy])

            # Check for bullet-boss collisions
            bullet = check_boss_collision(bullets, boss_pos)
            if bullet:
                bullets.remove(bullet)
                boss_health -= 10  # Reduce boss health
                if boss_health <= 0:
                    boss_alive = False  # Boss is defeated
                    boss_pos = [WIDTH // 2, HEIGHT // 4]  # Reset boss position
                    boss_health = 300  # Reset boss health

        # Draw health and shield bars
        draw_health_and_shield_bar(screen, player_health, player_shield)

        # Draw kill counter
        draw_kill_counter(screen, kill_count)

        # Draw boss health bar if the boss is alive
        if boss_alive:
            draw_boss_health_bar(screen, boss_health)

        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    game_over_screen()