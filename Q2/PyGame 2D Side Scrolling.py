import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()
# Screen dimensions
screen_width = 1080
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2D Side Scrolling Game')

player_image = pygame.image.load('Assests/main_player.png')
enemy_image = pygame.image.load('Assests/Enemy.png')
boss_image = pygame.image.load('Assests/Boss.png')
background_image = pygame.image.load('Assests/background.png')  # Replace with the correct path
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BOSS_COLOR = (0, 0, 255)

# Frame rate
clock = pygame.time.Clock()
fps = 60

# Game variables
player_speed = 5
jump_height = 15
gravity = 0.5
lives = 3
score = 0
enemy_kill_count = 0
kill_threshold = 10  # Number of enemies to kill before gaining a life
boss_health = 10  # Boss starts with 10 shots needed to kill in level 1
current_level = 1
boss_spawned = False

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (80, 70))  # Adjust size if needed
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 100)
        self.speed = player_speed
        self.jump = jump_height
        self.velocity_y = 0
        self.on_ground = False

    def update(self, keys):
        self.velocity_y += gravity

        # Move left and right
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

        # Jump
        if keys[K_SPACE] and self.on_ground:
            self.velocity_y = -self.jump
            self.on_ground = False

        self.rect.y += self.velocity_y

        # Check if on the ground
        if self.rect.bottom >= screen_height - 50:
            self.rect.bottom = screen_height - 50
            self.on_ground = True

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(enemy_image, (40, 60))  # Adjust size if needed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.x -= self.speed + current_level  # Increase speed with each level
        if self.rect.right < 0:
            self.kill()

# Boss projectile class (similar to the player's projectile but moves towards the player)
class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)  # Use a different color for boss's bullets
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10  # Boss projectiles move left (negative speed)

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:  # If the projectile goes off the screen, kill it
            self.kill()

# Boss enemy class
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(boss_image, (60, 80))  # Adjust size if needed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.shoot_timer = 0  # Timer to control shooting interval

    def update(self):
        self.rect.x -= self.speed + current_level  # Boss moves slower but is tougher
        if self.rect.right < 0:
            self.kill()

        # Shooting logic for the boss
        self.shoot_timer += 1
        if self.shoot_timer >= 60:  # Boss shoots every 60 frames (adjust as needed)
            boss_projectile = BossProjectile(self.rect.left, self.rect.centery)
            boss_projectile_group.add(boss_projectile)
            self.shoot_timer = 0  # Reset the shoot timer

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > screen_width:
            self.kill()

# Function to reset the level after player death
def reset_level():
    global enemy_kill_count, boss_spawned, enemy_group, boss_group, projectile_group, boss_health, current_level
    enemy_kill_count = 0
    boss_spawned = False
    player.rect.center = (screen_width // 2, screen_height - 100)
    enemy_group.empty()
    boss_group.empty()
    projectile_group.empty()
    boss_projectile_group.empty()

    # Set boss health based on the current level
    if current_level == 1:
        boss_health = 10
    elif current_level == 2:
        boss_health = 20
    elif current_level == 3:
        boss_health = 25

# Game over function
def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render('GAME OVER', True, WHITE)
    screen.blit(game_over_text, (screen_width // 2 - 180, screen_height // 2 - 60))

    font_small = pygame.font.SysFont(None, 36)
    restart_text = font_small.render('Press R to Restart or Q to Quit', True, WHITE)
    screen.blit(restart_text, (screen_width // 2 - 220, screen_height // 2 + 40))

    pygame.display.flip()

    # Wait for player to press R to restart or Q to quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    waiting = False  # Restart the game
                if event.key == K_q:
                    pygame.quit()
                    exit()

# Main game loop
def game_loop():
    global score, lives, enemy_kill_count, boss_health, boss_spawned, current_level, enemy_group, boss_group, projectile_group, boss_projectile_group
    screen.blit(background_image, (0, 0))  # Draw background

    # Sprite groups
    global player
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    enemy_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    projectile_group = pygame.sprite.Group()
    boss_projectile_group = pygame.sprite.Group()  # Group for boss's projectiles

    running = True
    while running:
        screen.blit(background_image, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_x:  # Shooting projectiles
                    projectile = Projectile(player.rect.right, player.rect.centery)
                    projectile_group.add(projectile)

        # Get key presses
        keys = pygame.key.get_pressed()

        # Update player, player projectiles, and boss projectiles
        player_group.update(keys)
        projectile_group.update()
        boss_projectile_group.update()

        # Spawn enemies regularly
        if not boss_spawned and random.randint(1, 100) == 1:
            enemy = Enemy(screen_width, screen_height - 100)
            enemy_group.add(enemy)

        # Spawn boss if enough enemies are killed
        if enemy_kill_count >= 20 and not boss_spawned:
            boss = Boss(screen_width, screen_height - 100)
            boss_group.add(boss)
            boss_spawned = True

        # Update enemies and boss
        enemy_group.update()
        boss_group.update()

        # Check collisions with regular enemies
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, projectile_group, True):
                score += 10
                enemy_kill_count += 1
                enemy.kill()

                # Gain an extra life every 10 kills
                if enemy_kill_count % kill_threshold == 0:
                    lives += 1

            if pygame.sprite.spritecollide(enemy, player_group, False):
                lives -= 1
                if lives > 0:
                    reset_level()  # Reset the level if player still has lives
                else:
                    game_over_screen()  # Call the game over screen
                    return  # End game loop
                enemy.kill()

        # Check collisions with boss
        for boss in boss_group:
            if pygame.sprite.spritecollide(boss, projectile_group, True):
                boss_health -= 1
                if boss_health <= 0:
                    score += 50  # Extra points for defeating the boss
                    boss.kill()
                    boss_spawned = False
                    current_level += 1
                    reset_level()  # Reset the level after defeating the boss

            if pygame.sprite.spritecollide(boss, player_group, False):
                lives -= 2  # Boss does more damage
                if lives > 0:
                    reset_level()  # Reset level upon boss hit if lives remain
                else:
                    game_over_screen()  # Call the game over screen
                    return  # End game loop

        # Check collisions between boss projectiles and player
        if pygame.sprite.spritecollide(player, boss_projectile_group, True):
            lives -= 1  # Reduce player's life if hit by a boss projectile
            if lives <= 0:
                game_over_screen()
                return  # End game loop

        # Draw sprites
        player_group.draw(screen)
        projectile_group.draw(screen)
        boss_projectile_group.draw(screen)  # Draw boss's projectiles
        enemy_group.draw(screen)
        boss_group.draw(screen)

        # Display score, lives, and level
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, BLACK)
        lives_text = font.render(f'Lives: {lives}', True, BLACK)
        level_text = font.render(f'Level: {current_level}', True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(level_text, (10, 90))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == '__main__':
    game_loop()
