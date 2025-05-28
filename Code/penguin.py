import pygame

class Penguin:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = None
        self.rect = None
        self.mask = None
        self.speed = 5
        self.load_image()

    def load_image(self):
        try:
            self.image = pygame.image.load('Assets/Sprites/sprite_penguin.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.center = (70, self.screen_height // 2)
            self.mask = pygame.mask.from_surface(self.image)
        except pygame.error as e:
            print(f"Error loading penguin image: {e}")
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 0, 255), (0, 0, 50, 50))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

    def reset_position(self):
        self.rect.center = (70, self.screen_height // 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)