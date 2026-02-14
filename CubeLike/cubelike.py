import pgzrun
import random

WIDTH = 800
HEIGHT = 600

MENU = 0
JOGANDO = 1
estado = MENU

menu_opcoes = ["INICIO", "MUSICA", "SAIR"]
menu _sele cionado = 0
musica_ligada = True

fundo = Act or("fundo")
fundo.pos = (WIDTH // 2, HEIGHT // 2)
 
# Animações do herói
heroi_i dle_frames = ["heroi_idle_1", "heroi_idle_2", "heroi_idle_3"]
heroi_correndo_frames = ["heroi_correndo_1", "heroi_correndo_2" ]
 
heroi = Actor(heroi_idle_frames[0])
heroi.pos = (WIDTH // 2, HEIGHT // 2)
velocidade_heroi = 5

anim_frame_index = 0
tempo_ul timo_frame = 0
vel_animacao = 0.1
anim_atual = "idle"

# Animação inimigo
inimigo_frames = ["inimigo_1", "inimigo_2"]
inimi gos = []
moedas = []
tempo_spa wn_inimigo = 0
tempo_spawn_moeda = 0
pont uacao = 0

# Controle de animação inimigos
tem po_ultimo_frame_inimigo = 0
vel_animacao_ inimigo = 0.2
# segundos entre frames do inimigo

def draw():
    screen.clear()
    if estado == MENU:
        screen.blit("menu", (-50, 0))
        dese nhar_menu()
    elif estado == JOGANDO:
        screen.blit("fundo", (0, 0))
        heroi. draw()
        for inimigo in inimigos:
            inimigo.draw()
        for moeda in moedas:
            moeda.draw()
        screen.draw.text(f"Moedas: {pontuacao}", (10, 10), fontsize=30, color="yellow")

def desenhar_menu():
    y_base = 250
    for i, opcao in enumerate(menu_opcoes):
        cor = "yellow" if i == menu_selecionado else "white"
        screen.draw.text(opcao, center=(WIDTH // 2, y_base + i * 40), fontsize=40, color=cor)

def on_key_down(key):
    global menu_selecionado, estado, musica_ligada

    if estado == MENU:
        if key == keys.UP:
            menu_selecionado = (menu_selecionado - 1) % len(menu_opcoes)
        elif key == keys.DOWN:
            menu_selecionado = (menu_selecionado + 1) % len(menu_opcoes)
        elif key == keys.RETURN:
            opcao = menu_opcoes[menu_selecionado]
            if opcao == "INICIO":
                sounds.moeda.play()
                iniciar_jogo()
            if opcao == "MUSICA":
                sounds.moeda.play()
                musica_ligada = not musica_ligada
                if musica_ligada:
                    music.play("musica")
                    musica_ligada = True
                else:
                    music.stop()
                    musica_ligada = False
            if opcao == "SAIR":
                sounds.moeda.play()
                quit()
    elif estado == JOGANDO:
        pass

def iniciar_jogo():
    global estado, inimigos, moedas, pontuacao, heroi, anim_frame_index, tempo_ultimo_frame, anim_atual, velocidade_heroi
    estado = JOGANDO
    pontuacao = 0
    inimigos.clear()
    moedas.clear()
    heroi.pos = (WIDTH // 2, HEIGHT // 2)
    anim_frame_index = 0
    tempo_ultimo_frame = 0
    anim_atual = "idle"
    heroi.image = heroi_idle_frames[0]
    velocidade_heroi = 1

def update(dt):
    global tempo_spawn_inimigo, tempo_spawn_moeda, pontuacao, velocidade_heroi
    global anim_frame_index, tempo_ultimo_frame, anim_atual
    global tempo_ultimo_frame_inimigo

    if estado == JOGANDO:
        # Herói animação e movimento
        movendo = False
        if keyboard.left or keyboard.right or keyboard.up or keyboard.down:
            movendo = True

        nova_anim = "correndo" if movendo else "idle"
        if nova_anim != anim_atual:
            anim_atual = nova_anim
            anim_frame_index = 0
            tempo_ultimo_frame = 0

        tempo_ultimo_frame += dt
        if tempo_ultimo_frame >= vel_animacao:
            tempo_ultimo_frame = 0
            if anim_atual == "idle":
                anim_frame_index = (anim_frame_index + 1) % len(heroi_idle_frames)
                heroi.image = heroi_idle_frames[anim_frame_index]
            else:
                anim_frame_index = (anim_frame_index + 1) % len(heroi_correndo_frames)
                heroi.image = heroi_correndo_frames[anim_frame_index]

        velocidade = velocidade_heroi
        if keyboard.left:
            heroi.x -= velocidade
        if keyboard.right:
            heroi.x += velocidade
        if keyboard.up:
            heroi.y -= velocidade
        if keyboard.down:
            heroi.y += velocidade

        heroi.x = max(0, min(WIDTH, heroi.x))
        heroi.y = max(0, min(HEIGHT, heroi.y))

        # Atualiza animação dos inimigos com timer
        tempo_ultimo_frame_inimigo += dt
        if tempo_ultimo_frame_inimigo >= vel_animacao_inimigo:
            tempo_ultimo_frame_inimigo = 0
            for inimigo in inimigos:
                inimigo.frame_index = (inimigo.frame_index + 1) % len(inimigo_frames)
                inimigo.image = inimigo_frames[inimigo.frame_index]

        movimentar_inimigos()
        checar_colisoes()

        tempo_spawn_inimigo += dt
        tempo_spawn_moeda += dt

        if tempo_spawn_inimigo > 2:
            spawn_inimigo()
            tempo_spawn_inimigo = 0

        if tempo_spawn_moeda > 3:
            spawn_moeda()
            tempo_spawn_moeda = 0

def spawn_inimigo():
    lado = random.choice(["top", "bottom", "left", "right"])
    if lado == "top":
        x = random.randint(0, WIDTH)
        y = 0
    elif lado == "bottom":
        x = random.randint(0, WIDTH)
        y = HEIGHT
    elif lado == "left":
        x = 0
        y = random.randint(0, HEIGHT)
    else:  # right
        x = WIDTH
        y = random.randint(0, HEIGHT)

    inimigo = Actor(inimigo_frames[0])
    inimigo.pos = (x, y)
    inimigo.frame_index = 0

    # Calcula vetor direção para herói na hora do spawn
    dx = heroi.x - x
    dy = heroi.y - y
    dist = (dx ** 2 + dy ** 2) ** 0.5
    if dist == 0:
        dist = 1  # evita divisão por zero

    direcao_x = dx / dist
    direcao_y = dy / dist
    inimigo.direcao = (direcao_x, direcao_y)

    inimigos.append(inimigo)
    
def spawn_moeda():
    x = random.randint(20, WIDTH - 20)
    y = random.randint(20, HEIGHT - 20)
    moeda = Actor("moeda")
    moeda.scale = 40.0
    moeda.pos = (x, y)
    moedas.append(moeda)

def movimentar_inimigos():
    velocidade = 2
    inimigos_para_remover = []
    for inimigo in inimigos:
        inimigo.x += inimigo.direcao[0] * velocidade
        inimigo.y += inimigo.direcao[1] * velocidade

        if (inimigo.x < -50 or inimigo.x > WIDTH + 50 or
            inimigo.y < -50 or inimigo.y > HEIGHT + 50):
            inimigos_para_remover.append(inimigo)

    for inimigo in inimigos_para_remover:
        inimigos.remove(inimigo)

def checar_colisoes():
    global pontuacao, velocidade_heroi
    for inimigo in inimigos:
        if heroi.colliderect(inimigo):
            print("Voce morreu!")
            voltar_menu()
            return

    for moeda in moedas[:]:
        if heroi.colliderect(moeda):
            sounds.moeda.play()
            moedas.remove(moeda)
            velocidade_heroi += 0.5 
            pontuacao += 1

def voltar_menu():
    global estado
    estado = MENU

music.play("musica")