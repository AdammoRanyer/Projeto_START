import pygame, os
from pygame.locals import *
pygame.init()

#nome do display
pygame.display.set_caption("Duel")

#definindo janela
resolucao = 3
janela = pygame.display.set_mode((256 * resolucao, 224 * resolucao))
janela_copia = janela.copy()

caminho_atual = os.path.dirname(__file__)
caminho_recursos = os.path.join(caminho_atual, "recursos")
caminho_imagens = os.path.join(caminho_recursos, "imagens")
sprites = pygame.image.load(os.path.join(caminho_imagens, "C1_pose1_spr.png"))
sprites = pygame.transform.scale(sprites, (sprites.get_size()[0] * resolucao, sprites.get_size()[1] * resolucao))
janela_copia.blit(sprites, (0, 0))



while True:
    event = pygame.event.wait()
    if event.type == VIDEORESIZE:
        janela = pygame.display.set_mode(event.dict["size"], RESIZABLE)
        janela.blit(pygame.transform.scale(janela_copia, (event.dict["size"])), (0, 0))
    if event.type == QUIT:
        pygame.display.quit()
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            pygame.display.quit()

    pygame.display.update()
    
