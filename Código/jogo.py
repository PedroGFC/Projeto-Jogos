import pygame
import sys

pygame.init()

largura_tela = 600
altura_tela = 400
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Pinguim Surfista")

#Cor do fundo
cor_fundo = (0, 0, 255) #Azul

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill(cor_fundo)

    pygame.display.flip()

pygame.quit()
sys.exit()
