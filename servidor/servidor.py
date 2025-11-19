# servidor.py
from xmlrpc.server import SimpleXMLRPCServer

game_state = {
    'score': 0,
    'lives': 3,
    'level': 1,
}

def get_game_state():
    print(f"SERVIDOR: Enviando estado: {game_state}")
    return game_state

def report_level_clear():
    global game_state
    
    game_state['level'] += 1 # se for = 3, o jogo acabou
    print(f"SERVIDOR: Nível avançado para {game_state['level']}")
        
    return game_state

def reset_game():
    global game_state
    game_state['score'] = 0
    game_state['lives'] = 3
    game_state['level'] = 1
    print("SERVIDOR: Jogo resetado.")
    return True

def report_collision(collision_type):
    global game_state
    
    if collision_type == "PASTILHA":
        game_state['score'] += 10
        print(f"SERVIDOR: Pastilha comida. Pontuação: {game_state['score']}")
    
    elif collision_type == "ENERGIZADOR":
        game_state['score'] += 50
        print(f"SERVIDOR: Energizador comido. Pontuação: {game_state['score']}")
        
    elif collision_type == "VILAO_COMIDO":
        game_state['score'] += 200
        print(f"SERVIDOR: Vilão comido. Pontuação: {game_state['score']}")

    elif collision_type == "BONUS":
        game_state['score'] += 500 
        print(f"SERVIDOR: Item bónus comido. Pontuação: {game_state['score']}")
    
    elif collision_type == "VILAO":
        game_state['lives'] -= 1
        print(f"SERVIDOR: Colisão com vilão. Vidas: {game_state['lives']}")
    
    return game_state

try:
    server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
    
    print("Servidor RPC iniciado em http://localhost:8000")
    print("Aguardando conexões do cliente...")

    server.register_function(get_game_state, "get_game_state")
    server.register_function(reset_game, "reset_game")
    server.register_function(report_collision, "report_collision")
    server.register_function(report_level_clear, "report_level_clear")

    server.serve_forever()

except Exception as e:
    print(f"Não foi possível iniciar o servidor: {e}")
    print("Verifique se a porta 8000 já não está em uso.")