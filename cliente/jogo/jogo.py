import pygame
import sys
import os 
from config import LARGURA, ALTURA, PRETO

# 1 = Parede, 2 = Pastilha, 3 = Energizador, 0 = Caminho Vazio
mapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 3, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 0, 1, 0, 0, 0, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 3, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 3, 1],
    [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

#  Tamanho do Bloco (Tile) 
NUM_COLUNAS = len(mapa[0])
NUM_LINHAS = len(mapa)
TILE_LARGURA = (LARGURA - 100) // NUM_COLUNAS
TILE_ALTURA = (ALTURA - 100) // NUM_LINHAS
TILE_SIZE = min(TILE_LARGURA, TILE_ALTURA)

# Margens para centralizar o mapa 
MARGEM_X = (LARGURA - (NUM_COLUNAS * TILE_SIZE)) // 2
MARGEM_Y = (ALTURA - (NUM_LINHAS * TILE_SIZE)) // 2

# Carregar imagens
try:
    ASSETS_PATH = "assets"
    
    # Parede
    wall_img = pygame.image.load(os.path.join(ASSETS_PATH, "wall.png")).convert_alpha()
    WALL_TEXTURE = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

    #  Pastilha
    pellet_img = pygame.image.load(os.path.join(ASSETS_PATH, "pellet.png")).convert_alpha()
    pellet_size = TILE_SIZE // 4 # A pastilha tem 1/4 do tamanho do bloco
    PELLET_TEXTURE = pygame.transform.scale(pellet_img, (pellet_size, pellet_size))

    #  Energizador
    power_img = pygame.image.load(os.path.join(ASSETS_PATH, "energizer.png")).convert_alpha()
    power_size = int(TILE_SIZE * 0.7) # O energizador tem 70% do tamanho do bloco
    POWER_TEXTURE = pygame.transform.scale(power_img, (power_size, power_size))

except FileNotFoundError as e:
    print(f"Erro! Textura não encontrada: {e}")
    pygame.quit()
    sys.exit()
except pygame.error as e:
    print(f"Erro ao carregar imagens do Pygame: {e}")
    pygame.quit()
    sys.exit()


def desenhar_mapa(tela):
    for id_linha, linha in enumerate(mapa):
        for id_coluna, tile in enumerate(linha):
            
            # Posição X e Y do *canto* do bloco
            x = MARGEM_X + (id_coluna * TILE_SIZE)
            y = MARGEM_Y + (id_linha * TILE_SIZE)

            if tile == 1:
                # "desenha" a textura da parede no (x, y)
                tela.blit(WALL_TEXTURE, (x, y))
                
            elif tile == 2:
                # Calcula o centro para "desenhar" a pastilha
                offset_x = (TILE_SIZE - PELLET_TEXTURE.get_width()) // 2
                offset_y = (TILE_SIZE - PELLET_TEXTURE.get_height()) // 2
                tela.blit(PELLET_TEXTURE, (x + offset_x, y + offset_y))

            elif tile == 3:
                # Calcula o centro para "desenhar" o energizador
                offset_x = (TILE_SIZE - POWER_TEXTURE.get_width()) // 2
                offset_y = (TILE_SIZE - POWER_TEXTURE.get_height()) // 2
                tela.blit(POWER_TEXTURE, (x + offset_x, y + offset_y))
            
            # Se o tile for 0, fundo fica preto

#  Loop Principal do Jogo 
def tela_jogo():
    pygame.init()
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Pacman DOOM - Jogo")
    
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False # Volta para o menu principal

        # "Renderização" 
        TELA.fill(PRETO)
        desenhar_mapa(TELA)
        pygame.display.flip()