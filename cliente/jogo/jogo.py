import pygame
import sys
import os 
import time 
from config import LARGURA, ALTURA, PRETO, BRANCO, VERDE
import random
from xmlrpc.client import ServerProxy
from .mapas import mapa_level_1, mapa_level_2

# Conexão com o servidor
try:
    server = ServerProxy('http://localhost:8000')
    print("CLIENTE: Conectado ao servidor RPC.")
except Exception as e: 
    print(f"CLIENTE: Erro ao conectar ao servidor: {e}")
    server = None

# Variáveis de Estado do Jogo 
DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"] 
POWER_UP_DURATION = 7000 # em ms
BONUS_LIFESPAN = 10000 # em ms
BONUS_SPAWN_INTERVAL = 20000 # em ms
game_state = {'score': 0, 'lives': 3, 'level': 1}
current_level = 1
current_map = None
player_pos = [14, 9]
player_speed = 1
PLAYER_START_POS = [14, 9]
current_direction = "NONE"
desired_direction = "NONE"
player_current_texture = None 
player_power_up_end_time = 0 

villains = []
VILLAIN_START_POS = [
    [8, 8], [8, 9], [8, 10], [9, 9]
]

bonus_item = {
    "active": False,
    "pos": [0, 0],
    "despawn_time": 0
}
next_bonus_spawn_time = 0
valid_spawn_points = [] 

# Resolução
NUM_COLUNAS = len(mapa_level_1[0])
NUM_LINHAS = len(mapa_level_1)
TILE_LARGURA = (LARGURA - 100) // NUM_COLUNAS
TILE_ALTURA = (ALTURA - 100) // NUM_LINHAS
TILE_SIZE = min(TILE_LARGURA, TILE_ALTURA)
MARGEM_X = (LARGURA - (NUM_COLUNAS * TILE_SIZE)) // 2
MARGEM_Y = (ALTURA - (NUM_LINHAS * TILE_SIZE)) // 2

# Carregamento das texturas 
try:
    pygame.font.init() 
    UI_FONT = pygame.font.Font(None, 36)

    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    ASSETS_PATH = os.path.join(os.path.dirname(caminho_atual), "assets")
    
    wall_img = pygame.image.load(os.path.join(ASSETS_PATH, "wall.png")).convert_alpha()
    WALL_TEXTURE = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))

    pellet_img = pygame.image.load(os.path.join(ASSETS_PATH, "pellet.png")).convert_alpha()
    pellet_size = TILE_SIZE // 4
    PELLET_TEXTURE = pygame.transform.scale(pellet_img, (pellet_size, pellet_size))

    energizer = pygame.image.load(os.path.join(ASSETS_PATH, "energizer.png")).convert_alpha()
    energizer_size = int(TILE_SIZE * 0.7)
    ENERGIZER_TEXTURE = pygame.transform.scale(energizer, (energizer_size, energizer_size))

    player_size = int(TILE_SIZE * 0.9)
    PLAYER_TEXTURES = {
        "UP": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "pacman_up.png")).convert_alpha(), (player_size, player_size)),
        "DOWN": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "pacman_down.png")).convert_alpha(), (player_size, player_size)),
        "LEFT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "pacman_left.png")).convert_alpha(), (player_size, player_size)),
        "RIGHT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "pacman_right.png")).convert_alpha(), (player_size, player_size)),
        "NONE": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "pacman_right.png")).convert_alpha(), (player_size, player_size)), # default
    }
    player_current_texture = PLAYER_TEXTURES["RIGHT"]

    villain_size = int(TILE_SIZE * 0.9)
    VILLAIN_TEXTURES = []

    # Vilão 1
    VILLAIN_TEXTURES.append({
        "UP": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_1_up.png")).convert_alpha(), (villain_size, villain_size)),
        "DOWN": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_1_down.png")).convert_alpha(), (villain_size, villain_size)),
        "LEFT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_1_left.png")).convert_alpha(), (villain_size, villain_size)),
        "RIGHT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_1_right.png")).convert_alpha(), (villain_size, villain_size)),
    })
    
    # Vilão 2
    VILLAIN_TEXTURES.append({
        "UP": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_2_up.png")).convert_alpha(), (villain_size, villain_size)),
        "DOWN": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_2_down.png")).convert_alpha(), (villain_size, villain_size)),
        "LEFT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_2_left.png")).convert_alpha(), (villain_size, villain_size)),
        "RIGHT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_2_right.png")).convert_alpha(), (villain_size, villain_size)),
    })
    
    # Vilão 3
    VILLAIN_TEXTURES.append({
        "UP": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_3_up.png")).convert_alpha(), (villain_size, villain_size)),
        "DOWN": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_3_down.png")).convert_alpha(), (villain_size, villain_size)),
        "LEFT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_3_left.png")).convert_alpha(), (villain_size, villain_size)),
        "RIGHT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_3_right.png")).convert_alpha(), (villain_size, villain_size)),
    })
    
    # Vilão 4
    VILLAIN_TEXTURES.append({
        "UP": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_4_up.png")).convert_alpha(), (villain_size, villain_size)),
        "DOWN": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_4_down.png")).convert_alpha(), (villain_size, villain_size)),
        "LEFT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_4_left.png")).convert_alpha(), (villain_size, villain_size)),
        "RIGHT": pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH, "villain_4_right.png")).convert_alpha(), (villain_size, villain_size)),
    })
    
    # Textura do vilão quando o player come o energizador
    villain_fright_img = pygame.image.load(os.path.join(ASSETS_PATH, "villain_frightened.png")).convert_alpha()
    VILLAIN_FRIGHTENED_TEXTURE = pygame.transform.scale(villain_fright_img, (villain_size, villain_size))

    villain_fright_img = pygame.image.load(os.path.join(ASSETS_PATH, "villain_frightened.png")).convert_alpha()
    VILLAIN_FRIGHTENED_TEXTURE = pygame.transform.scale(villain_fright_img, (villain_size, villain_size))

    bonus_img = pygame.image.load(os.path.join(ASSETS_PATH, "bonus.png")).convert_alpha()
    bonus_size = int(TILE_SIZE * 0.9)
    BONUS_TEXTURE = pygame.transform.scale(bonus_img, (bonus_size, bonus_size))

except FileNotFoundError as e:
    print(f"Erro! Textura não encontrada: {e}")
    pygame.quit()
    sys.exit()


# Desenha as informações do jogo (game_state)
def desenhar_ui(tela):
    global game_state
    
    # Formata o texto
    texto_vidas = f"VIDAS: {game_state.get('lives', 0)}"
    texto_score = f"PONTOS: {game_state.get('score', 0)}"
    
    # Renderiza o texto
    txt_surf_vidas = UI_FONT.render(texto_vidas, True, BRANCO)
    txt_surf_score = UI_FONT.render(texto_score, True, BRANCO)
    
    # Desenha a contagem de vidas
    pos_x_vidas = MARGEM_X
    pos_y_vidas = MARGEM_Y - txt_surf_vidas.get_height() - 10
    
    # Posição da pontuação
    pos_x_score = LARGURA - MARGEM_X - txt_surf_score.get_width()
    pos_y_score = MARGEM_Y - txt_surf_score.get_height() - 10
    
    # Atualiza o texto na tela
    area_vidas = pygame.Rect(pos_x_vidas, pos_y_vidas, txt_surf_vidas.get_width(), txt_surf_vidas.get_height())
    area_score = pygame.Rect(pos_x_score, pos_y_score, txt_surf_score.get_width(), txt_surf_score.get_height())
    tela.fill(PRETO, area_vidas)
    tela.fill(PRETO, area_score)
    tela.blit(txt_surf_vidas, (pos_x_vidas, pos_y_vidas))
    tela.blit(txt_surf_score, (pos_x_score, pos_y_score))

def desenhar_mapa(tela):
    global current_map
    for id_linha, linha in enumerate(current_map):
        for id_coluna, tile in enumerate(linha):
            x = MARGEM_X + (id_coluna * TILE_SIZE)
            y = MARGEM_Y + (id_linha * TILE_SIZE)
            if tile == 0:
                pygame.draw.rect(tela, PRETO, (x, y, TILE_SIZE, TILE_SIZE))
            elif tile == 1:
                tela.blit(WALL_TEXTURE, (x, y))
            elif tile == 2:
                pygame.draw.rect(tela, PRETO, (x, y, TILE_SIZE, TILE_SIZE))
                offset_x = (TILE_SIZE - PELLET_TEXTURE.get_width()) // 2
                offset_y = (TILE_SIZE - PELLET_TEXTURE.get_height()) // 2
                tela.blit(PELLET_TEXTURE, (x + offset_x, y + offset_y))
            elif tile == 3:
                pygame.draw.rect(tela, PRETO, (x, y, TILE_SIZE, TILE_SIZE))
                offset_x = (TILE_SIZE - ENERGIZER_TEXTURE.get_width()) // 2
                offset_y = (TILE_SIZE - ENERGIZER_TEXTURE.get_height()) // 2
                tela.blit(ENERGIZER_TEXTURE, (x + offset_x, y + offset_y))

def desenhar_mapa_tile(tela, linha, coluna):
    x = MARGEM_X + (coluna * TILE_SIZE)
    y = MARGEM_Y + (linha * TILE_SIZE)
    tile = current_map[linha][coluna]

    if tile == 0:
        pygame.draw.rect(tela, PRETO, (x, y, TILE_SIZE, TILE_SIZE))
    elif tile == 1:
        tela.blit(WALL_TEXTURE, (x, y))
    elif tile == 2:
        pygame.draw.rect(tela, PRETO, (x, y, TILE_SIZE, TILE_SIZE))
        offset_x = (TILE_SIZE - PELLET_TEXTURE.get_width()) // 2
        offset_y = (TILE_SIZE - PELLET_TEXTURE.get_height()) // 2
        tela.blit(PELLET_TEXTURE, (x + offset_x, y + offset_y))
    elif tile == 3:
        pygame.draw.rect(tela, PRETO, (x, y, TILE_SIZE, TILE_SIZE))
        offset_x = (TILE_SIZE - ENERGIZER_TEXTURE.get_width()) // 2
        offset_y = (TILE_SIZE - ENERGIZER_TEXTURE.get_height()) // 2
        tela.blit(ENERGIZER_TEXTURE, (x + offset_x, y + offset_y))

def desenhar_jogador(tela, pos):
    global player_current_texture 
    
    pixel_x = MARGEM_X + (pos[1] * TILE_SIZE)
    pixel_y = MARGEM_Y + (pos[0] * TILE_SIZE)
    offset_x = (TILE_SIZE - player_current_texture.get_width()) // 2 
    offset_y = (TILE_SIZE - player_current_texture.get_height()) // 2 
    
    desenhar_mapa_tile(tela, pos[0], pos[1]) 
    
    tela.blit(player_current_texture, (pixel_x + offset_x, pixel_y + offset_y))

def desenhar_villains(tela):
    for v in villains:
        pos = v['pos']
        
        desenhar_mapa_tile(tela, pos[0], pos[1]) 
        
        if v['state'] == "EATEN": continue
        
        texture = None
        if v['state'] == "FRIGHTENED":
            texture = VILLAIN_FRIGHTENED_TEXTURE
        else: 
            texture_set = VILLAIN_TEXTURES[v['id']] 
            direction = v['direction']
            if direction not in texture_set: # textura default é o "down"
                direction = "DOWN" 
            if direction == "NONE":
                texture = texture_set["DOWN"]
            else:
                texture = texture_set[direction]
        
        pixel_x = MARGEM_X + (pos[1] * TILE_SIZE)
        pixel_y = MARGEM_Y + (pos[0] * TILE_SIZE)
        offset_x = (TILE_SIZE - texture.get_width()) // 2
        offset_y = (TILE_SIZE - texture.get_height()) // 2
        
        tela.blit(texture, (pixel_x + offset_x, pixel_y + offset_y))

def check_wall_collision(mapa, next_pos):
    linha = next_pos[0]
    coluna = next_pos[1]
    if mapa[linha][coluna] == 1:
        return True
    return False

def check_level_clear(mapa):
    for linha in mapa:
        for tile in linha:
            if tile == 2 or tile == 3:
                return False
    return True

def desenhar_bonus_item(tela):
    if bonus_item["active"]:
        pos = bonus_item["pos"]
        pixel_x = MARGEM_X + (pos[1] * TILE_SIZE)
        pixel_y = MARGEM_Y + (pos[0] * TILE_SIZE)
        
        # Atualiza o mapa inteiro pra colocar o tile correto por baixo (pode melhorar mas to com preguiça)
        desenhar_mapa_tile(tela, pos[0], pos[1]) 
        
        # Desenha o item bonus
        offset_x = (TILE_SIZE - BONUS_TEXTURE.get_width()) // 2
        offset_y = (TILE_SIZE - BONUS_TEXTURE.get_height()) // 2
        tela.blit(BONUS_TEXTURE, (pixel_x + offset_x, pixel_y + offset_y))
        
        # Retorna a tile pra a lista de atualização
        return pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
    
    return None 

def update_bonus_item(now):
    global next_bonus_spawn_time
    
    # Verifica se o itme bonus deve aparecer
    if bonus_item["active"] == False:
        if now > next_bonus_spawn_time and valid_spawn_points:
            print("CLIENTE: Item de bonus apareceu!")
            bonus_item["active"] = True
            bonus_item["pos"] = random.choice(valid_spawn_points)
            bonus_item["despawn_time"] = now + BONUS_LIFESPAN
            # Define o timer para a próxima tentativa de spawn
            next_bonus_spawn_time = now + BONUS_SPAWN_INTERVAL
            return True 
        
    # Verifica se o item bonus deve desaparecer
    else:
        if now > bonus_item["despawn_time"]:
            print("CLIENTE: Item de bonus desapareceu.")
            bonus_item["active"] = False
            return True
            
    return False

def handle_player_bonus_collision(now): # Dava pra colocar no handle_item_collision() mas acho que fica mais facil de ver assim
    global game_state, next_bonus_spawn_time
    if bonus_item["active"] and player_pos == bonus_item["pos"]:
        bonus_item["active"] = False
        # Define um cooldown para o próximo spawn
        next_bonus_spawn_time = now + BONUS_SPAWN_INTERVAL
        
        if server:
            game_state = server.report_collision("BONUS")
        print("CLIENTE: Item bonus comido!")
        
        # Atualiza a UI 
        desenhar_ui(pygame.display.get_surface())
        pygame.display.update(pygame.Rect(0, 0, LARGURA, MARGEM_Y))
        
        return True # Comido (precisa redesenhar o tile)
    return False

def handle_item_collision(mapa, pos):
    global player_power_up_end_time, game_state
    
    linha = pos[0]
    coluna = pos[1]
    tile_value = mapa[linha][coluna]
    
    item_eaten = False
    
    if tile_value == 2: # Pastilha
        mapa[linha][coluna] = 0
        if server:
            game_state = server.report_collision("PASTILHA")
        item_eaten = True

    elif tile_value == 3: # Energizador
        mapa[linha][coluna] = 0
        if server:
            game_state = server.report_collision("ENERGIZADOR")

        player_power_up_end_time = pygame.time.get_ticks() + POWER_UP_DURATION
        for v in villains:
            if v['state'] != "EATEN":
                v['state'] = "FRIGHTENED"
        item_eaten = True
    
    if item_eaten: # Toda vez que comer um item, checa se o nível foi completo.
        return check_level_clear(mapa)
    return False

def load_level(level_number):
    global current_level, current_map, player_pos, current_direction, desired_direction
    global villains, player_power_up_end_time, game_state
    global bonus_item, next_bonus_spawn_time, valid_spawn_points 
    
    # Comm server
    if server:
        if level_number == 1:
            server.reset_game()
        game_state = server.get_game_state()
    else:
        # Server falhou por algum motivo
        print("CLIENTE: Modo offline ativado, verifique se o servidor está aberto.")
        if level_number == 1:
            game_state = {'score': 0, 'lives': 3, 'level': 1}
    
    # Reseta estados do jogo
    current_level = game_state.get('level', 1)
    player_pos = list(PLAYER_START_POS)
    current_direction = "NONE"
    desired_direction = "NONE"
    player_power_up_end_time = 0 
    
    # Reseta bonus
    bonus_item["active"] = False
    next_bonus_spawn_time = pygame.time.get_ticks() + BONUS_SPAWN_INTERVAL
    valid_spawn_points.clear()
    
    # Troca (avança) o mapa (nível) 
    villains.clear()
    if current_level == 1: 
        current_map = [row[:] for row in mapa_level_1]
    elif current_level == 2:
        current_map = [row[:] for row in mapa_level_2] 
    else:
        print("VOCÊ VENCEU O JOGO!")
        return False
        
    # Carrega os vilões
    for i, start_pos in enumerate(VILLAIN_START_POS):
        if i >= len(VILLAIN_TEXTURES): 
            print(f"Aviso: Não há conjunto de texturas para o vilão {i+1}")
            break
            
        villains.append({
            'id': i, # 0,1,2,3
            'pos': list(start_pos),
            'old_pos': list(start_pos),
            'start_pos': list(start_pos),
            'direction': "NONE",
            'state': "NORMAL",
            'respawn_time': 0 
        })
            
    # Encontra locais válidos pro item bonus spawnar
    for r, row in enumerate(current_map):
        for c, tile in enumerate(row):
            if tile == 0 or tile == 2: # 0 = vazio, 2 = pastilha
                valid_spawn_points.append([r, c])
                
    print(f"Carregando Nível {level_number}...")
    return True

def calculate_next_pos(pos, direction):
    next_pos = list(pos)
    if direction == "UP":
        next_pos[0] -= player_speed
    elif direction == "DOWN":
        next_pos[0] += player_speed
    elif direction == "LEFT":
        next_pos[1] -= player_speed
    elif direction == "RIGHT":
        next_pos[1] += player_speed
    return next_pos

def get_chase_direction(ghost_pos, target_pos, valid_moves): # Pra IA do nível 2, usa a dist de manhattan
    best_move = random.choice(valid_moves) # Padrão (caso todas sejam iguais)
    min_dist = float('inf')
    
    for move in valid_moves:
        # Calcula onde o vilão estaria se fizesse este movimento
        next_pos = calculate_next_pos(ghost_pos, move)
        
        # |x1 - x2| + |y1 - y2|
        dist = abs(next_pos[0] - target_pos[0]) + abs(next_pos[1] - target_pos[1])
        
        if dist < min_dist:
            min_dist = dist
            best_move = move
            
    return best_move

def update_villains(current_time, level):
    global current_map, player_pos
    
    for v in villains:
        if v['state'] == "EATEN":
            if current_time > v['respawn_time']:
                print("CLIENTE: Vilão renasceu!")
                v['pos'] = list(v['start_pos'])
                v['old_pos'] = list(v['start_pos'])
                v['state'] = "NORMAL"
                v['direction'] = "NONE"
            continue 
            
        v['old_pos'] = list(v['pos'])

        valid_moves = get_valid_moves(v['pos'], current_map)
        
        if not valid_moves:
            v['direction'] = "NONE"
            continue

        new_direction = v['direction']
        
        should_chase = False
        
        if level == 2 and (v['id'] == 0 or v['id'] == 1) and v['state'] == "NORMAL":
            should_chase = True
            
        if should_chase:
            new_direction = get_chase_direction(v['pos'], player_pos, valid_moves)
        else:
            next_pos_current = calculate_next_pos(v['pos'], v['direction'])
            hit_wall = check_wall_collision(current_map, next_pos_current)
            
            if v['direction'] == "NONE" or hit_wall:
                new_direction = random.choice(valid_moves)
            else:
                if len(valid_moves) > 2 and random.random() < 0.3:
                    new_direction = random.choice(valid_moves)
                else:
                    new_direction = v['direction']

        v['direction'] = new_direction

        final_next_pos = calculate_next_pos(v['pos'], v['direction'])
        if not check_wall_collision(current_map, final_next_pos):
            v['pos'] = final_next_pos

def handle_player_villain_collision(current_time):
    global player_pos, current_direction, desired_direction, game_state
    
    for v in villains:
        if player_pos == v['pos']:
            # se ta com o energizador, come
            if v['state'] == "FRIGHTENED":
                v['state'] = "EATEN"
                v['respawn_time'] = current_time + 5000 
                if server:
                    game_state = server.report_collision("VILAO_COMIDO")
                return "VILLAIN_EATEN"
            # senão, morre
            elif v['state'] == "NORMAL":
                if server:
                    game_state = server.report_collision("VILAO")
                
                print(f"CLIENTE: Colisão com vilão. Vidas: {game_state.get('lives', 0)}")
                
                player_pos = list(PLAYER_START_POS)
                current_direction = "NONE"
                desired_direction = "NONE"
                
                return "PLAYER_DIED"
                
    return "NONE"

def get_valid_moves(pos, current_map):
    valid_moves = []
    for d in DIRECTIONS:
        # Verifica se o movimento é válido
        next_pos = calculate_next_pos(pos, d)
        if not check_wall_collision(current_map, next_pos):
            valid_moves.append(d)
    return valid_moves

def desenhar_tela(tela, player_pos):
    tela.fill(PRETO)
    desenhar_mapa(tela)
    desenhar_ui(tela)
    desenhar_villains(tela)
    desenhar_jogador(tela, player_pos)
    pygame.display.flip() 

def tela_jogo():
    pygame.init()
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Pacman DOOM - Jogo")
    
    global player_pos, current_direction, desired_direction, player_power_up_end_time, game_state, player_current_texture
    
    # Começa o nível 1 (e o gamestate do server)  
    if not load_level(1):
        return 

    clock = pygame.time.Clock()
    
    player_move_cooldown = 150 # Velocidade do Jogador 
    last_player_move_time = 0
    
    villain_move_cooldown = 250 # Velocidade do Vilão 
    last_villain_move_time = 0

    # Desenho inicial
    desenhar_tela(TELA, player_pos)

    rodando = True
    while rodando:
        
        # Timers e flags
        now = pygame.time.get_ticks() # Tempo atual em ms
        old_player_pos = list(player_pos)
        level_cleared = False
        player_moved = False
        villains_moved = False
        villain_eaten = False
        power_up_expired = False
        villain_respawned = False 
        bonus_item_changed = False 
        
        # Verifica se o energizador acabou
        if player_power_up_end_time != 0 and now > player_power_up_end_time:
            print("CLIENTE: Power-up acabou.")
            player_power_up_end_time = 0
            power_up_expired = True # Redesenha vilões
            for v in villains:
                if v['state'] == "FRIGHTENED":
                    v['state'] = "NORMAL"

        # Atualiza item bonus
        bonus_item_changed = update_bonus_item(now)

        # Input do jogador
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False # Volta ao menu principal
                # Buffer de input que nem o pacman original
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    desired_direction = "UP"
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    desired_direction = "DOWN"
                elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    desired_direction = "LEFT"
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    desired_direction = "RIGHT"

                elif evento.key == pygame.K_n: # Apertar "N" passa de nível automaticamente 
                    print("CHEAT: Forçando próximo nível...")
                    level_cleared = True 
                    rodando = False

        # Movimento do jogador
        if now - last_player_move_time > player_move_cooldown:
            last_player_move_time = now
            
            # Tenta mover na direção desejada
            if desired_direction != "NONE":
                next_pos = calculate_next_pos(player_pos, desired_direction)
                if not check_wall_collision(current_map, next_pos):
                    player_pos = next_pos
                    current_direction = desired_direction
                    player_moved = True
                    player_current_texture = PLAYER_TEXTURES[current_direction] 

            # Se não conseguiu, tenta mover na direção atual
            if not player_moved and current_direction != "NONE":
                next_pos = calculate_next_pos(player_pos, current_direction)
                if not check_wall_collision(current_map, next_pos):
                    player_pos = next_pos
                    player_moved = True
                else: # Bateu na parede, para
                    current_direction = "NONE"
            
            # Se o jogador se moveu, verifica colisões com itens
            if player_moved:
                level_cleared = handle_item_collision(current_map, player_pos)
                if handle_player_bonus_collision(now):
                    bonus_item_changed = True

        # Movimento dos vilões
        if now - last_villain_move_time > villain_move_cooldown:
            last_villain_move_time = now
            
            # Guarda estados antigos para verificar renascimento
            old_states = [v['state'] for v in villains]
            
            # Atualiza o movimento dos vilões
            update_villains(now, current_level) 
            
            new_states = [v['state'] for v in villains]
            
            # Verifica se alguém renasceu (para redesenhar)
            if "EATEN" in old_states and "NORMAL" in new_states:
                villain_respawned = True

            # Verifica se alguém se moveu (para redesenhar)
            villains_moved = any(v['pos'] != v['old_pos'] for v in villains)

        # Colisão jogador/vilão 
        collision_type = handle_player_villain_collision(now) 
        
        if collision_type == "PLAYER_DIED":
            
            # Verifica game over (server)
            if game_state.get('lives', 0) <= 0:
                print("CLIENTE: Fim de Jogo!")
                fonte_aviso = pygame.font.Font(None, 74)
                aviso = fonte_aviso.render("FIM DE JOGO", True, (255, 0, 0))
                TELA.blit(aviso, (LARGURA//2 - aviso.get_width()//2, ALTURA//2 - aviso.get_height()//2))
                desenhar_ui(TELA)
                pygame.display.flip()
                time.sleep(3) 
                rodando = False 
                continue 
            
            # Se não for Fim de Jogo, reseta posição dos vilões e jogador
            print("CLIENTE: Resetando posições dos vilões.")
            for v in villains:
                v['pos'] = list(v['start_pos'])
                v['old_pos'] = list(v['start_pos'])
                v['state'] = "NORMAL"
                v['direction'] = "NONE"
    
            desenhar_tela(TELA, player_pos)

            time.sleep(0.5) 
            continue 
            
        elif collision_type == "VILLAIN_EATEN":
            villain_eaten = True

        # Redesenhos parciais
        if player_moved or villains_moved or villain_eaten or power_up_expired or villain_respawned or bonus_item_changed:
            rects_to_update = []
            ui_rect = pygame.Rect(0, 0, LARGURA, MARGEM_Y)

            # Apaga rastro do jogador
            if player_moved:
                desenhar_mapa_tile(TELA, old_player_pos[0], old_player_pos[1])
                rects_to_update.append(pygame.Rect(
                    MARGEM_X + (old_player_pos[1] * TILE_SIZE),
                    MARGEM_Y + (old_player_pos[0] * TILE_SIZE),
                    TILE_SIZE, TILE_SIZE))
            
            # Apaga rastro dos vilões
            if villains_moved or power_up_expired or villain_respawned:
                for v in villains:
                    if (villains_moved and v['pos'] != v['old_pos']) or power_up_expired or (villain_respawned and v['pos'] == v['start_pos']):
                        desenhar_mapa_tile(TELA, v['old_pos'][0], v['old_pos'][1])
                        rects_to_update.append(pygame.Rect(
                            MARGEM_X + (v['old_pos'][1] * TILE_SIZE),
                            MARGEM_Y + (v['old_pos'][0] * TILE_SIZE),
                            TILE_SIZE, TILE_SIZE
                        ))
            
            # Limpa o tile do bonus (se ele desapareceu ou foi comido)
            if bonus_item_changed and not bonus_item["active"]:
                desenhar_mapa_tile(TELA, bonus_item["pos"][0], bonus_item["pos"][1])
                rects_to_update.append(pygame.Rect(
                    MARGEM_X + (bonus_item["pos"][1] * TILE_SIZE),
                    MARGEM_Y + (bonus_item["pos"][0] * TILE_SIZE),
                    TILE_SIZE, TILE_SIZE
                ))

            # Desenha os vilões na nova posição
            if villains_moved or power_up_expired or villain_eaten or villain_respawned:
                for v in villains:
                    pos = v['pos']
                    pixel_x = MARGEM_X + (pos[1] * TILE_SIZE)
                    pixel_y = MARGEM_Y + (pos[0] * TILE_SIZE)
                    
                    desenhar_mapa_tile(TELA, pos[0], pos[1])
                    
                    if v['state'] != "EATEN":
                        texture = None
                        if v['state'] == "FRIGHTENED":
                            texture = VILLAIN_FRIGHTENED_TEXTURE
                        else: 
                            texture_set = VILLAIN_TEXTURES[v['id']]
                            direction = v['direction']
                            if direction == "NONE": 
                                direction = "DOWN"
                            texture = texture_set[direction]

                        offset_x = (TILE_SIZE - texture.get_width()) // 2
                        offset_y = (TILE_SIZE - texture.get_height()) // 2
                        TELA.blit(texture, (pixel_x + offset_x, pixel_y + offset_y))
                    
                    rects_to_update.append(pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))

            # Desenha o jogador na nova posição
            if player_moved:
                desenhar_jogador(TELA, player_pos)
                rects_to_update.append(pygame.Rect(
                    MARGEM_X + (player_pos[1] * TILE_SIZE),
                    MARGEM_Y + (player_pos[0] * TILE_SIZE),
                    TILE_SIZE, TILE_SIZE
                ))
            
            # Desenha o item bonus (se ativo
            bonus_rect = desenhar_bonus_item(TELA)
            if bonus_rect:
                rects_to_update.append(bonus_rect)
            
            # Desenha a UI
            desenhar_ui(TELA)
            rects_to_update.append(ui_rect)
            
            # Faz as atualizações parciais
            if rects_to_update:
                pygame.display.update(rects_to_update)

       # Transição de nível
        if level_cleared:
            print("NÍVEL CONCLUÍDO!")
            
            # Mostra mensagem de Nível Concluído
            fonte_aviso = pygame.font.Font(None, 74)
            aviso = fonte_aviso.render(f"Nível {current_level} Concluído!", True, (255,255,0))
            TELA.blit(aviso, (LARGURA//2 - aviso.get_width()//2, ALTURA//2 - aviso.get_height()//2))
            pygame.display.flip()
            time.sleep(2)

            # Determina o próximo nível (comunica com o server)
            novo_nivel = current_level
            if server:
                print("CLIENTE: Informando servidor sobre fim do nível...")
                game_state = server.report_level_clear() 
                novo_nivel = game_state.get('level', current_level + 1)
            else:
                novo_nivel += 1
            
            if novo_nivel > 2: # Zerou o jogo
                print("CLIENTE: Jogo Zerado!")
                
                TELA.fill(PRETO)
                
                # Renderiza mensagens de Vitória
                fonte_grande = pygame.font.Font(None, 80)
                texto_win = fonte_grande.render("VITÓRIA!", True, VERDE)
                texto_msg = UI_FONT.render("Parabéns! Completou todos os níveis.", True, BRANCO)
                texto_retorno = UI_FONT.render("Voltando ao menu...", True, BRANCO)
                
                # Centraliza e desenha
                TELA.blit(texto_win, (LARGURA//2 - texto_win.get_width()//2, ALTURA//2 - 60))
                TELA.blit(texto_msg, (LARGURA//2 - texto_msg.get_width()//2, ALTURA//2 + 20))
                TELA.blit(texto_retorno, (LARGURA//2 - texto_retorno.get_width()//2, ALTURA//2 + 60))
                
                # Mostra a pontuação final
                desenhar_ui(TELA) 
                pygame.display.flip()
                
                time.sleep(5)
                
                rodando = False 
                continue

            rodando = load_level(novo_nivel)
            
            if rodando:
                # Desenho inicial do novo nível
                desenhar_tela(TELA, player_pos)
        
        # FPS
        clock.tick(60)