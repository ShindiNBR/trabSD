import pygame
import sys
from config import LARGURA, ALTURA, BRANCO, PRETO, AMARELO

def tela_creditos():
    pygame.init()
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Créditos")

    FONTE = pygame.font.Font(None, 36)

    texto = [
        "CRÉDITOS",
        "Use as setas CIMA e BAIXO para rolar.", 
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
        "", 
        "Pressione ESC para voltar ao menu."
    ]

    scroll_y = 0  
    scroll_speed = 30  
    espacamento_linha = 60
    margem_topo = 100

    altura_total_texto = margem_topo + (len(texto) * espacamento_linha)
    
    max_scroll_negativo = ALTURA - altura_total_texto - 50 # 50 de margem inferior
    
    if max_scroll_negativo > 0:
        max_scroll_negativo = 0

    rodando = True
    while rodando:
    
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

                elif evento.key == pygame.K_UP:
                    scroll_y += scroll_speed
                    if scroll_y > 0:
                        scroll_y = 0
                
                elif evento.key == pygame.K_DOWN:
                    scroll_y -= scroll_speed
                    if scroll_y < max_scroll_negativo:
                        scroll_y = max_scroll_negativo

        TELA.fill(PRETO)
        
        for i, linha in enumerate(texto):
            cor = BRANCO
            if "Pressione ESC" in linha or "Use as setas" in linha:
                cor = AMARELO
                
            txt = FONTE.render(linha, True, cor)
            
            pos_y = margem_topo + (i * espacamento_linha) + scroll_y
            TELA.blit(txt, (50, pos_y))

        pygame.display.flip()