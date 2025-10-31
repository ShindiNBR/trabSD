import pygame
import sys
from config import LARGURA, ALTURA, TITULO, BRANCO, PRETO, AMARELO

pygame.init()

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

FONTE = pygame.font.Font(None, 60)
FONTE_MENOR = pygame.font.Font(None, 40)

opcoes = ["Iniciar Jogo", "Ajuda", "Sobre", "Crédito", "Sair"]
selecionado = 0

def desenhar_menu():
    TELA.fill(PRETO)
    titulo = FONTE.render("Pacman DOOM", True, AMARELO)
    TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 100))

    for i, opcao in enumerate(opcoes):
        cor = AMARELO if i == selecionado else BRANCO
        texto = FONTE_MENOR.render(opcao, True, cor)
        TELA.blit(texto, (LARGURA//2 - texto.get_width()//2, 250 + i*60))

    pygame.display.flip()

def menu_principal():
    global selecionado
    while True:
        desenhar_menu()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    if opcoes[selecionado] == "Iniciar Jogo":
                        print("Iniciando jogo...")
                        return "JOGO"
                    elif opcoes[selecionado] == "Ajuda":
                        return "AJUDA"
                    elif opcoes[selecionado] == "Sobre":
                        return "SOBRE"
                    elif opcoes[selecionado] == "Crédito":
                        return "CREDITO"
                    elif opcoes[selecionado] == "Sair":
                        pygame.quit()
                        sys.exit()
