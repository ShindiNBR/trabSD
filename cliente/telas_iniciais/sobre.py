import pygame
import sys
from config import LARGURA, ALTURA, BRANCO, PRETO, AMARELO

def tela_sobre():
    pygame.init()
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Sobre")

    FONTE_TITULO = pygame.font.Font(None, 48)
    FONTE = pygame.font.Font(None, 26)

    texto = [
        "SOBRE O JOGO",
        "Pacman DOOM",
        "Imitação do clássico jogo Pacman utilizando texturas do jogo DOOM.",
        "Jogo distribuído desenvolvido para o trabalho da disciplina de: ",
        "Disciplina: 6920 - Sistemas Distribuídos",
        "Curso de Bacharelado em Ciência da Computação",
        "Departamento de Informática (DIN)",
        "Universidade Estadual de Maringá (UEM)",
        "",
        "Pressione ESC para voltar ao menu."
    ]

    rodando = True
    while rodando:
        TELA.fill(PRETO)
        
        txt_titulo = FONTE_TITULO.render(texto[0], True, AMARELO)
        TELA.blit(txt_titulo, (LARGURA//2 - txt_titulo.get_width()//2, 80))

        for i, linha in enumerate(texto[1:], start=1):
            cor = BRANCO
            if "Pressione ESC" in linha:
                cor = AMARELO
                
            txt = FONTE.render(linha, True, cor)
            if "Disciplina" in linha or "Curso" in linha or "Departamento" in linha or "Universidade" in linha:
                 TELA.blit(txt, (LARGURA//2 - txt.get_width()//2, 100 + i*40))
            else:
                TELA.blit(txt, (50, 100 + i*40))


        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False