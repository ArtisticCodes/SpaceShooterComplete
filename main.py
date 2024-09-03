import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800,500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 36)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player settings
#Student will remove quotes from numbers
player_width = 90
player_height = 100

player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 7
score=0

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 10
bullets = []

# alien settings
alien_width = 50
alien_height = 50
alien_speed = 5
aliens = []

# Load images
background_img = pygame.image.load("background.jpg").convert()
alien_img = pygame.image.load("alien.png")
alien_img = pygame.transform.scale(alien_img, (alien_width, alien_height))
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))

# Load sounds
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Play background music indefinitely
collision_sound = pygame.mixer.Sound("collision_sound.mp3")

# Function to draw bullets
def draw_bullet(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

# Function to draw aliens
def draw_aliens(aliens):
    for alien in aliens:
        screen.blit(alien_img, alien)

# Function to display the score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


# Game Loop
def game_loop():
    global player_x, bullets, aliens,score

    #student will remove quotes from True

    running = True
    frame_count = 0

    while running==True:
        screen.blit(background_img, (0, 0))  # Draw background image
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height))

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Move bullets
        for bullet in bullets:
            bullet.y -= bullet_speed

        # Remove off-screen bullets
        bullets = [bullet for bullet in bullets if bullet.y > 0]

        # Generate new aliens
        if frame_count % 50 == 0:
            alien_x = random.randint(0, WIDTH - alien_width)
            aliens.append(pygame.Rect(alien_x, -alien_height, alien_width, alien_height))
        frame_count += 1

        # Move aliens
        for alien in aliens:
            alien.y += alien_speed

        # Check for collisions
        for alien in aliens:
            if player_y < alien.y + alien_height and player_y + player_height > alien.y:
                if player_x < alien.x + alien_width and player_x + player_width > alien.x:
                    running = False  # Collision detected, end game

        # Remove off-screen aliens
        aliens = [alien for alien in aliens if alien.y < HEIGHT]

        # Check bullet collision with aliens
        for bullet in bullets:
            for alien in aliens:
                if bullet.colliderect(alien):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    collision_sound.play()  # Play collision sound
                    score += 1  # Increase score by 1
                    break

        # Draw player, bullets, and aliens
        screen.blit(player_img, (player_x, player_y))
        draw_bullet(bullets)
        draw_aliens(aliens)

         # Display the score
        display_score(score)

        # Update the display
        pygame.display.flip()
        
        # Control game speed
        clock.tick(FPS)

    pygame.quit()

# Run the game
game_loop()
