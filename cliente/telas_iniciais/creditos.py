import pygame
import sys

def tela_creditos():
    pygame.init()
    LARGURA, ALTURA = 800, 600
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Créditos")

    FONTE = pygame.font.Font(None, 36)
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)

    texto = [
        "CRÉDITOS",
        "Integrantes do trabalho:",
        "   Rodrigo Kenji Olini Watanabe - RA:123630",
        "   Gabriel Oliveira Gomes - RA:125154",
        "Linguagem de programação utilizada:",
        "   Python",
        "Protocolo de comunicação utilizado:",
        "   RPC (Remote Procedure Call)",
        "Bibliotecas utilizadas:",
        "   Pygame para a interface gráfica e manipulação de eventos",
        "   xmlrpc para comunicação cliente-servidor",
        "''Ainda bem que ele não ta cobrando estética'' - Rodrigo",
        "''Por quê?'' - Gabriel",
        "''Porquê tá muito feio kkkkkk'' - Rodrigo",
        "Pressione ESC para voltar ao menu."
    ]

    rodando = True
    while rodando:
        TELA.fill(PRETO)
        for i, linha in enumerate(texto):
            txt = FONTE.render(linha, True, BRANCO)
            TELA.blit(txt, (50, 100 + i*60))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False    