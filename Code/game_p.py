import pygame
import sys
import os
import random

pygame.init()

# Screen settings
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Surfing Penguin")

# --- Game States ---
STATE_MAIN_MENU = "main_menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
current_state = STATE_MAIN_MENU

# --- Fonts ---
# Usaremos a fonte existente para score e game over message, e criaremos novas para título e menu
try:
    score_font = pygame.font.Font(None, 36) # Fonte do código original
    title_font = pygame.font.Font(None, 60)
    menu_font = pygame.font.Font(None, 40)
except Exception as e:
    print(f"Erro ao carregar fonte padrão: {e}. Usando fallback.")
    score_font = pygame.font.Font(None, 36) # Fallback
    title_font = pygame.font.Font(None, 60)
    menu_font = pygame.font.Font(None, 40)


# --- Caminhos para as imagens ---
assets_folder = 'Assets'

# Função para carregar imagens (evita repetição)
def load_image(file_name, scale_to=None, convert_alpha=False, convert=False): #
    path = os.path.join(assets_folder, file_name) #
    try:
        image = pygame.image.load(path) #
        if convert_alpha:
            image = image.convert_alpha() #
        elif convert:
            image = image.convert() #
        if scale_to:
            image = pygame.transform.scale(image, scale_to) #
        return image
    except pygame.error as e:
        print(f"Error: Image '{file_name}' not found or could not be loaded from {path} - {e}") #
        pygame.quit() #
        sys.exit() #

# Load images
# Tratamento de erro para garantir que 'running' seja definido antes do loop principal
running = True # Definido como True por padrão
try:
    penguin_img = load_image('sprite_penguin.png', scale_to=(50, 50), convert_alpha=True) #
    hole_img_original = load_image('sprite_hole.png', convert_alpha=True) #
    hole_img = pygame.transform.scale(hole_img_original, (70, 100)) #
    bg_image = load_image('background_ice.png', scale_to=(screen_width, screen_height), convert=True) #
except SystemExit:
    running = False # Impede o início do loop se as imagens falharem

# Penguin
penguin_rect = penguin_img.get_rect() if 'penguin_img' in locals() else pygame.Rect(0,0,0,0) # Define um rect padrão se a imagem falhar
player_speed = 5 #

# Obstacle Class
class Obstacle(pygame.sprite.Sprite): #
    def __init__(self, image, speed): #
        super().__init__() #
        self.image = image #
        self.rect = self.image.get_rect() #
        self.rect.x = screen_width #
        max_y_pos = screen_height - self.rect.height #
        self.rect.y = random.randint(0, max_y_pos if max_y_pos > 0 else 0) #
        self.speed = speed #

    def update(self): #
        self.rect.x -= self.speed #
        if self.rect.right < 0: #
            self.kill() #

# Grupos de Sprites
obstacles = pygame.sprite.Group() #
all_sprites = pygame.sprite.Group() # (usado para adicionar buracos, mas não para desenhar/atualizar tudo)

# Obstacle settings
obstacle_speed = 4 #
obstacle_spawn_rate = 1800 #
obstacle_timer = pygame.USEREVENT + 1 #
obstacle_timer_active = False # Timer não ativo inicialmente

# Game variables
score = 0 #

# --- Função para Desenhar Texto ---
def draw_text(text, font, color, surface, x, y, center_aligned=True):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center_aligned:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

# --- Função para Resetar/Inicializar o Jogo ---
def initialize_game():
    global score, player_speed, obstacle_timer_active
    global penguin_rect # Assegura que estamos modificando o penguin_rect global


    penguin_rect.center = (70, screen_height // 2) #
    obstacles.empty()
    all_sprites.empty() # Limpa os buracos de all_sprites também

    score = 0 #
    # player_speed = 5 # Já definido globalmente, resetar se puder mudar

    # Ativa e reseta o timer de obstáculos
    pygame.time.set_timer(obstacle_timer, 0) # Limpa qualquer timer pendente
    pygame.time.set_timer(obstacle_timer, obstacle_spawn_rate) #
    obstacle_timer_active = True

# Main game loop
clock = pygame.time.Clock() #

# Variáveis de Botão (serão redefinidas no loop para obter Rects atualizados)
button_start = None
button_quit = None
button_resume = None
button_restart_pause = None
button_main_menu_pause = None
button_restart_gameover = None
button_main_menu_gameover = None


while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Botão esquerdo
                mouse_clicked = True

        # --- Eventos específicos do estado PLAYING ---
        if current_state == STATE_PLAYING:
            if event.type == obstacle_timer and obstacle_timer_active: # (modificado com obstacle_timer_active)
                new_hole = Obstacle(hole_img, obstacle_speed) #
                obstacles.add(new_hole) #
                all_sprites.add(new_hole) #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    current_state = STATE_PAUSED
                    obstacle_timer_active = False # Pausa o spawn de obstáculos
        
        # --- Eventos específicos do estado PAUSED (além de cliques) ---
        elif current_state == STATE_PAUSED:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p: # Atalho para Resume
                    current_state = STATE_PLAYING
                    obstacle_timer_active = True # Reativa o spawn

    # --- Lógica e Desenho baseados no Estado Atual ---
    if current_state == STATE_MAIN_MENU:
        screen.fill((20, 20, 80)) # Cor de fundo para o menu
        draw_text("Surfing Penguin", title_font, (220, 220, 255), screen, screen_width / 2, screen_height / 4)
        
        button_start = draw_text("Iniciar Jogo", menu_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2)
        button_quit = draw_text("Sair", menu_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 + 70)

        if mouse_clicked:
            if button_start and button_start.collidepoint(mouse_pos):
                initialize_game()
                current_state = STATE_PLAYING
            if button_quit and button_quit.collidepoint(mouse_pos):
                running = False

    elif current_state == STATE_PLAYING:
        # Keyboard movement controls
        keys = pygame.key.get_pressed() #
        if keys[pygame.K_UP] and penguin_rect.top > 0: #
            penguin_rect.y -= player_speed #
        if keys[pygame.K_DOWN] and penguin_rect.bottom < screen_height: #
            penguin_rect.y += player_speed #

        # Update
        obstacles.update() #

        # Aumentar a pontuação
        score += 1 # (mantendo a lógica original de pontuação por frame)

        # Collision detection
        for hole in obstacles: #
            if penguin_rect.colliderect(hole.rect): #
                current_state = STATE_GAME_OVER
                obstacle_timer_active = False
                break #
        
        # Draw everything
        screen.blit(bg_image, (0, 0)) #
        screen.blit(penguin_img, penguin_rect) #
        obstacles.draw(screen) #

        # Draw Score
        score_text_surface = score_font.render(f"Score: {score // 20}", True, (0,0,0)) #
        screen.blit(score_text_surface, (10, 10)) #

    elif current_state == STATE_PAUSED:
        # Desenha a tela de jogo por baixo
        screen.blit(bg_image, (0, 0))
        screen.blit(penguin_img, penguin_rect)
        obstacles.draw(screen)
        score_text_surface = score_font.render(f"Score: {score // 20}", True, (0,0,0))
        screen.blit(score_text_surface, (10, 10))

        # Adiciona uma camada semi-transparente
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # RGBA
        screen.blit(overlay, (0,0))

        draw_text("PAUSADO", title_font, (255, 255, 0), screen, screen_width / 2, screen_height / 4)
        button_resume = draw_text("Continuar (P ou Esc)", menu_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 - 30)
        button_restart_pause = draw_text("Reiniciar", menu_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 + 40)
        button_main_menu_pause = draw_text("Menu Principal", menu_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 + 110)

        if mouse_clicked:
            if button_resume and button_resume.collidepoint(mouse_pos):
                current_state = STATE_PLAYING
                obstacle_timer_active = True
            if button_restart_pause and button_restart_pause.collidepoint(mouse_pos):
                initialize_game()
                current_state = STATE_PLAYING
            if button_main_menu_pause and button_main_menu_pause.collidepoint(mouse_pos):
                current_state = STATE_MAIN_MENU
                obstacle_timer_active = False 
                pygame.time.set_timer(obstacle_timer, 0) # Desativa o timer ao voltar para o menu

    elif current_state == STATE_GAME_OVER:
        # Desenha a tela de jogo por baixo (opcional)
        screen.blit(bg_image, (0, 0))
        screen.blit(penguin_img, penguin_rect)
        obstacles.draw(screen)

        # Adiciona uma camada semi-transparente
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # Mais escuro para game over
        screen.blit(overlay, (0,0))
        
        game_over_text_surface = title_font.render("GAME OVER", True, (255, 0, 0)) # Usando title_font para "GAME OVER"
        text_rect = game_over_text_surface.get_rect(center=(screen_width/2, screen_height/3)) # (adaptado)
        screen.blit(game_over_text_surface, text_rect)
        
        draw_text(f"Seu Score: {score // 20}", menu_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2)
        
        button_restart_gameover = draw_text("Reiniciar", menu_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 + 70)
        button_main_menu_gameover = draw_text("Menu Principal", menu_font, (255, 255, 255), screen, screen_width / 2, screen_height / 2 + 140)

        if mouse_clicked:
            if button_restart_gameover and button_restart_gameover.collidepoint(mouse_pos):
                initialize_game()
                current_state = STATE_PLAYING
            if button_main_menu_gameover and button_main_menu_gameover.collidepoint(mouse_pos):
                current_state = STATE_MAIN_MENU
                obstacle_timer_active = False
                pygame.time.set_timer(obstacle_timer, 0) # Desativa o timer ao voltar para o menu

    pygame.display.flip() #
    clock.tick(60) #

pygame.quit() #
sys.exit() #