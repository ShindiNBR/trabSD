import pygame
import sys

def tela_ajuda():
    pygame.init()
    LARGURA, ALTURA = 800, 600
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Ajuda")

    FONTE = pygame.font.Font(None, 36)
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)

    texto = [
        "AJUDA",
        "Use as setas ou WASD para mover o personagem .",
        "Evite os vilões e colete todos os itens para ganhar pontos!",
        "Utilize power-ups para conseguir derrotar os inimigos e ganhar pontos extra!"
        "Ao coletar todos os itens, você avança para a próxima fase.",
        "Cuidado: se um inimigo tocar em você, perderá uma vida!",
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
