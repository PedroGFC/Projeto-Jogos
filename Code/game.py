import pygame
import sys
import os
from penguin import Penguin
from obstacle import Obstacle

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen_width = 600
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Surfing Penguin")
        pygame.display.set_icon(pygame.image.load("Assets/Sprites/sprite_penguin.png"))

        self.STATE_MAIN_MENU = "main_menu"
        self.STATE_PLAYING = "playing"
        self.STATE_PAUSED = "paused"
        self.STATE_GAME_OVER = "game_over"
        self.current_state = self.STATE_MAIN_MENU

        self.phases = [
            {"bg": "background_ice.png", "obstacle_img": "sprite_hole.png", "obstacle_speed": 10, "spawn_rate": 1650, "bg_color": (20, 20, 80)},
            {"bg": "background_ocean.png", "obstacle_img": "shark.png", "obstacle_speed": 12, "spawn_rate": 1400, "bg_color": (0, 50, 120)},
            {"bg": "background_volcano.png", "obstacle_img": "fire.png", "obstacle_speed": 14, "spawn_rate": 1250, "bg_color": (120, 30, 0)}
        ]
        self.current_phase = 0
        self.phase_score_thresholds = [150, 300]

        font_path = os.path.join('Assets/Fonts', 'Daydream.ttf')
        self.score_font = pygame.font.Font(font_path, 12)
        self.title_font = pygame.font.Font(font_path, 24)
        self.menu_font = pygame.font.Font(font_path, 16)

        self.penguin = Penguin(self.screen_width, self.screen_height)
        self.obstacles = pygame.sprite.Group()

        self.score = 0
        self.obstacle_timer_active = False
        self.obstacle_timer = pygame.USEREVENT + 1

        self.bg_scroll_x = 0
        self.bg_speed = 2

        self.music_tracks = [
            'Assets/Sounds/bg_ice.wav',
            'Assets/Sounds/bg_ocean.wav',
            'Assets/Sounds/bg_volcano.wav'
        ]
        self.menu_music = 'Assets/Sounds/menu_theme.wav'
        self.hit_sound = pygame.mixer.Sound('Assets/Sounds/hit.wav')

        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.play(-1)

        self.load_phase_assets()

        self.clock = pygame.time.Clock()

    def load_phase_assets(self):
        phase = self.phases[self.current_phase]
        try:
            self.bg_image = pygame.image.load(os.path.join('Assets/Images', phase["bg"]))
            self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
            self.bg_image = self.bg_image.convert()
        except pygame.error as e:
            print(f"Error loading background: {e}")
            self.bg_image = pygame.Surface((self.screen_width, self.screen_height))
            self.bg_image.fill(phase["bg_color"])

        self.obstacle_speed = phase["obstacle_speed"]
        self.obstacle_spawn_rate = phase["spawn_rate"]
        self.current_obstacle_img = phase["obstacle_img"]
        self.bg_speed = self.obstacle_speed // 3

    def initialize_game(self):
        self.score = 0
        self.current_phase = 0
        self.bg_scroll_x = 0
        self.load_phase_assets()
        self.penguin.reset_position()
        self.obstacles.empty()

        pygame.time.set_timer(self.obstacle_timer, 0)
        self.obstacle_timer_active = False

        pygame.mixer.music.load(self.music_tracks[self.current_phase])
        pygame.mixer.music.play(-1)

        self.screen.fill((255, 255, 255))
        self.draw_text("Fase 1 - Ice", self.title_font, (0, 0, 0), self.screen, self.screen_width / 2, self.screen_height / 2)
        pygame.display.flip()
        pygame.time.delay(2000)

        pygame.time.set_timer(self.obstacle_timer, self.obstacle_spawn_rate)
        self.obstacle_timer_active = True

    def check_phase_transition(self):
        if self.current_phase < len(self.phase_score_thresholds):
            if self.score // 20 >= self.phase_score_thresholds[self.current_phase]:
                self.current_phase += 1
                self.load_phase_assets()
                self.obstacles.empty()

                pygame.time.set_timer(self.obstacle_timer, 0)
                self.obstacle_timer_active = False

                pygame.mixer.music.load(self.music_tracks[self.current_phase])
                pygame.mixer.music.play(-1)

                self.screen.fill((255, 255, 255))
                phase_text = f"Fase {self.current_phase + 1} - {'Ice' if self.current_phase == 0 else 'Ocean' if self.current_phase == 1 else 'Volcano'}"
                self.draw_text(phase_text, self.title_font, (0, 0, 0), self.screen, self.screen_width / 2, self.screen_height / 2)
                pygame.display.flip()
                pygame.time.delay(2000)

                pygame.time.set_timer(self.obstacle_timer, self.obstacle_spawn_rate)
                self.obstacle_timer_active = True

    def draw_text(self, text, font, color, surface, x, y, center_aligned=True):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if center_aligned:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)
        return text_rect

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

            if self.current_state == self.STATE_PLAYING:
                if event.type == self.obstacle_timer and self.obstacle_timer_active:
                    new_obstacle = Obstacle(
                        'Assets/Sprites',
                        self.screen_width,
                        self.screen_height,
                        self.obstacle_speed,
                        self.current_phase
                    )
                    self.obstacles.add(new_obstacle)

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_p):
                    self.current_state = self.STATE_PAUSED
                    self.obstacle_timer_active = False

            elif self.current_state == self.STATE_PAUSED:
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_p):
                    self.current_state = self.STATE_PLAYING
                    self.obstacle_timer_active = True

        if mouse_clicked:
            if self.current_state == self.STATE_MAIN_MENU:
                if hasattr(self, 'button_start') and self.button_start.collidepoint(mouse_pos):
                    self.initialize_game()
                    self.current_state = self.STATE_PLAYING
                    pygame.mixer.music.load(self.music_tracks[self.current_phase])
                    pygame.mixer.music.play(-1)

                if hasattr(self, 'button_quit') and self.button_quit.collidepoint(mouse_pos):
                    return False

            elif self.current_state == self.STATE_PAUSED:
                if hasattr(self, 'button_resume') and self.button_resume.collidepoint(mouse_pos):
                    self.current_state = self.STATE_PLAYING
                    self.obstacle_timer_active = True
                if hasattr(self, 'button_restart_pause') and self.button_restart_pause.collidepoint(mouse_pos):
                    self.initialize_game()
                    self.current_state = self.STATE_PLAYING
                    pygame.mixer.music.load(self.music_tracks[self.current_phase])
                    pygame.mixer.music.play(-1)
                if hasattr(self, 'button_main_menu_pause') and self.button_main_menu_pause.collidepoint(mouse_pos):
                    self.current_state = self.STATE_MAIN_MENU
                    pygame.time.set_timer(self.obstacle_timer, 0)
                    pygame.mixer.music.load(self.menu_music)
                    pygame.mixer.music.play(-1)

            elif self.current_state == self.STATE_GAME_OVER:
                if hasattr(self, 'button_restart_gameover') and self.button_restart_gameover.collidepoint(mouse_pos):
                    self.initialize_game()
                    self.current_state = self.STATE_PLAYING
                    pygame.mixer.music.load(self.music_tracks[self.current_phase])
                    pygame.mixer.music.play(-1)
                if hasattr(self, 'button_main_menu_gameover') and self.button_main_menu_gameover.collidepoint(mouse_pos):
                    self.current_state = self.STATE_MAIN_MENU
                    pygame.time.set_timer(self.obstacle_timer, 0)
                    pygame.mixer.music.load(self.menu_music)
                    pygame.mixer.music.play(-1)

        return True

    def update(self):
        if self.current_state == self.STATE_PLAYING:
            keys = pygame.key.get_pressed()
            self.penguin.update(keys)
            self.obstacles.update()

            self.score += 1
            self.check_phase_transition()

            for obstacle in self.obstacles:
                if pygame.sprite.collide_mask(self.penguin, obstacle):
                    self.hit_sound.play()
                    self.current_state = self.STATE_GAME_OVER
                    self.obstacle_timer_active = False
                    break

            self.bg_scroll_x -= self.bg_speed
            if self.bg_scroll_x <= -self.screen_width:
                self.bg_scroll_x = 0

    def draw(self):
        if self.current_state == self.STATE_MAIN_MENU:
            self.screen.fill((20, 20, 80))
            self.draw_text("Surfing Penguin", self.title_font, (220, 220, 255), self.screen, self.screen_width / 2, self.screen_height / 4)
            self.button_start = self.draw_text("Iniciar Jogo", self.menu_font, (255, 255, 255), self.screen, self.screen_width / 2, self.screen_height / 2)
            self.button_quit = self.draw_text("Sair", self.menu_font, (255, 255, 255), self.screen, self.screen_width / 2, self.screen_height / 2 + 70)
        else:
            self.screen.blit(self.bg_image, (self.bg_scroll_x, 0))
            self.screen.blit(self.bg_image, (self.bg_scroll_x + self.screen_width, 0))
            self.penguin.draw(self.screen)
            self.obstacles.draw(self.screen)
            self.draw_text(f"Score: {self.score // 20}", self.score_font, (0, 0, 0), self.screen, 10, 10, False)
            if self.current_state in [self.STATE_PLAYING, self.STATE_PAUSED]:
                self.draw_text(f"Fase: {self.current_phase + 1}", self.score_font, (0, 0, 0), self.screen, 10, 40, False)

            if self.current_state == self.STATE_PAUSED:
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, (0,0))
                self.draw_text("PAUSADO", self.title_font, (255, 255, 0), self.screen, self.screen_width / 2, self.screen_height / 4)
                self.button_resume = self.draw_text("Continuar (P ou Esc)", self.menu_font, (255, 255, 255), self.screen, self.screen_width / 2, self.screen_height / 2 - 30)
                self.button_restart_pause = self.draw_text("Reiniciar", self.menu_font, (255, 255, 255), self.screen, self.screen_width / 2, self.screen_height / 2 + 40)
                self.button_main_menu_pause = self.draw_text("Menu Principal", self.menu_font, (255, 255, 255), self.screen, self.screen_width / 2, self.screen_height / 2 + 110)

            elif self.current_state == self.STATE_GAME_OVER:
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (0,0))
                self.draw_text("GAME OVER", self.title_font, (255, 0, 0), self.screen, self.screen_width / 2, self.screen_height / 3)
                self.draw_text(f"Seu Score: {self.score // 20}", self.menu_font, (255, 255, 255), self.screen, self.screen_width / 2, self.screen_height / 2)
                self.button_restart_gameover = self.draw_text("Reiniciar", self.menu_font, (255, 255, 255), self.screen, self.screen_width / 2, self.screen_height / 2 + 70)
                self.button_main_menu_gameover = self.draw_text("Menu Principal", self.menu_font, (255, 255, 255), self.screen, self.screen_width / 2, self.screen_height / 2 + 140)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()