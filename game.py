import pygame
import sys
import os

pygame.init()

# Screen settings
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Surfing Penguin")

# Colors
bg_color = (0, 0, 255)  # Blue

# Load penguin sprite
try:
    penguin = pygame.image.load(os.path.join('Assets', 'sprite_penguin.png'))
    penguin = pygame.transform.scale(penguin, (50, 50))  # Resize if needed
except:
    print("Error: Penguin image not found in Assets folder!")
    pygame.quit()
    sys.exit()


# Penguin initial position
penguin_rect = penguin.get_rect()
penguin_rect.center = (70, 200)

# Movement speed
speed = 5

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and penguin_rect.top > 0:
        penguin_rect.y -= speed
    if keys[pygame.K_DOWN] and penguin_rect.bottom < screen_height:
        penguin_rect.y += speed

    # Draw everything
    screen.fill(bg_color)
    screen.blit(penguin, penguin_rect)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
sys.exit()
