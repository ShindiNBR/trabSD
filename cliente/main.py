from telas_iniciais.menu import menu_principal
from telas_iniciais.ajuda import tela_ajuda
from telas_iniciais.sobre import tela_sobre
from telas_iniciais.creditos import tela_creditos
# from jogo import tela_jogo 

def main():
    while True:
        escolha = menu_principal()

        if escolha == "AJUDA":
            tela_ajuda()

        elif escolha == "SOBRE":
            tela_sobre()

        elif escolha == "CREDITO":
            tela_creditos()

        # elif escolha == "JOGO":
        #     tela_jogo()

        elif escolha == "SAIR":
            break


if __name__ == "__main__":
    main()
