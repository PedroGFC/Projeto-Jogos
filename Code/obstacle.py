import pygame
import random
import os

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, assets_folder, screen_width, screen_height, speed, phase):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.phase = phase  # (0, 1 or 2)
        self.load_image(assets_folder)
        self.reset_position()

    def load_image(self, assets_folder):
        # Image for each level
        if self.phase == 1:  # Level 2 - shark
            image_file = 'shark.png'
            target_size = (100, 60)
        elif self.phase == 2:  # Level 3 - fire
            image_file = 'fire.png'
            target_size = (60, 80)
        else:  # Level 1 - hole
            image_file = 'sprite_hole.png'
            target_size = (70, 100)

        try:
            image_path = os.path.join(assets_folder, image_file)
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, target_size)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
        except pygame.error as e:
            print(f"Error loading obstacle image: {e}")
            # Placeholder for each level
            self.image = pygame.Surface(target_size, pygame.SRCALPHA)
            if self.phase == 1:  # Level 2 - blue (shark)
                color = (0, 0, 255)
            elif self.phase == 2:  # Level 3 - red (fire)
                color = (255, 0, 0)
            else:  # Level 1 - black (hole)
                color = (0, 0, 0)
            pygame.draw.rect(self.image, color, (0, 0, *target_size))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

    def reset_position(self):
        self.rect.x = self.screen_width
        max_y_pos = self.screen_height - self.rect.height
        self.rect.y = random.randint(0, max_y_pos if max_y_pos > 0 else 0)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
