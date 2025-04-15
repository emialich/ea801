from machine import Pin, SoftI2C, ADC, PWM
import utime
import ssd1306
import neopixel
import random

# Configuração do SoftI2C para o display OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))

# Inicialização do display OLED SSD1306
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuração da matriz de LEDs WS2812B (5x5)
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Definindo a matriz de LEDs
LED_MATRIX = [
    [24, 23, 22, 21, 20],
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]
]

# Configuração do joystick
vrx = ADC(Pin(27))  # Movimento horizontal
vry = ADC(Pin(26))  # Movimento vertical

# Configuração dos botões
button_a = Pin(5, Pin.IN, Pin.PULL_UP)  # Botão A (start)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)  # Botão B (variar cor)

# Configuração do buzzer
buzzer = PWM(Pin(21))

# Desenhos pré-setados
desenhos = [

    # Cruz com um traço vermelho e outro azul
    [
        (2, 0, (255, 0, 0)), (2, 1, (255, 0, 0)), (2, 2, (255, 0, 0)), (2, 3, (255, 0, 0)), (2, 4, (255, 0, 0)),
        (0, 2, (0, 0, 255)), (1, 2, (0, 0, 255)), (3, 2, (0, 0, 255)), (4, 2, (0, 0, 255))
    ],

    # Novo desenho ajustado conforme especificado
    [
        (0, 0, (255, 255, 0)), (0, 1, (255, 255, 0)), (1, 0, (255, 255, 0)), (1, 1, (255, 255, 0)),  # Amarelo
        (4, 0, (255, 0, 0)), (4, 1, (255, 0, 0)), (3, 0, (255, 0, 0)), (3, 1, (255, 0, 0)),  # Vermelho
        (0, 4, (0, 0, 255)), (0, 3, (0, 0, 255)), (1, 4, (0, 0, 255)), (1, 3, (0, 0, 255))  # Azul
    ],

    # Seta
    [
        (2, 0, (255, 255, 0)), (1, 1, (255, 255, 0)), (2, 1, (255, 255, 0)), (3, 1, (255, 255, 0)),
        (0, 2, (255, 255, 0)), (1, 2, (255, 255, 0)), (2, 2, (255, 255, 0)), (3, 2, (255, 255, 0)), (4, 2, (255, 255, 0))
    ],


    # Coração preenchido
    [
        (2, 0, (255, 0, 0)),
        (1, 1, (255, 0, 0)), (2, 1, (255, 0, 0)), (3, 1, (255, 0, 0)),
        (0, 2, (255, 0, 0)), (1, 2, (255, 0, 0)), (2, 2, (255, 0, 0)), (3, 2, (255, 0, 0)), (4, 2, (255, 0, 0)),
        (0, 3, (255, 0, 0)), (1, 3, (255, 0, 0)), (2, 3, (255, 0, 0)), (3, 3, (255, 0, 0)), (4, 3, (255, 0, 0)),
        (1, 4, (255, 0, 0)), (2, 4, (255, 0, 0)), (3, 4, (255, 0, 0))
    ],

    # Quadrado colorido
    [
        (0, 0, (255, 0, 0)), (0, 1, (255, 0, 0)), (0, 2, (255, 0, 0)), (0, 3, (255, 0, 0)), (0, 4, (255, 0, 0)),
        (1, 0, (0, 255, 0)), (1, 4, (0, 255, 0)),
        (2, 0, (0, 0, 255)), (2, 4, (0, 0, 255)),
        (3, 0, (255, 255, 0)), (3, 4, (255, 255, 0)),
        (4, 0, (255, 0, 255)), (4, 1, (255, 0, 255)), (4, 2, (255, 0, 255)), (4, 3, (255, 0, 255)), (4, 4, (255, 0, 255))
    ],

    # Letra "L"
    [
        (0, 0, (0, 255, 255)), (1, 0, (0, 255, 255)), (2, 0, (0, 255, 255)), (3, 0, (0, 255, 255)),
        (4, 0, (0, 255, 255)), (4, 1, (0, 255, 255)), (4, 2, (0, 255, 255)), (4, 3, (0, 255, 255)), (4, 4, (0, 255, 255))
    ]
]

# Função para desenhar o desenho na matriz de LEDs
def desenhar_desenho(desenho, brilho=0.5):
    np.fill((0, 0, 0))  # Apagar todos os LEDs
    for (x, y, cor) in desenho:
        np[LED_MATRIX[y][x]] = (int(cor[0] * brilho), int(cor[1] * brilho), int(cor[2] * brilho))
    np.write()

# Função para mostrar mensagem no display OLED
def mostrar_mensagem(mensagem, score=None, tempo=None):
    oled.fill(0)
    oled.text(mensagem, 0, 0)
    if score is not None:
        oled.text("Score: {}%".format(score), 0, 20)
    if tempo is not None:
        oled.text("Tempo: {:.1f}s".format(tempo), 0, 40)
    oled.show()

# Função para mostrar contagem regressiva no display OLED
def contagem_regressiva(segundos):
    for i in range(segundos, 0, -1):
        oled.fill(0)
        oled.text("Tempo: {}".format(i), 0, 0)
        oled.text("Atencao!", 0, 20)
        oled.text("Memorize", 0, 40)
        oled.show()
        utime.sleep(1)

# Função para apagar a matriz de LEDs
def apagar_matriz():
    np.fill((0, 0, 0))
    np.write()

# Função para tocar música no buzzer
def tocar_musica():
    notas = [262, 294, 330, 349, 392, 440, 494, 523]  # Notas da escala C
    duracao = 0.2  # Duração de cada nota
    for nota in notas:
        buzzer.freq(nota)
        buzzer.duty_u16(1000)  # Volume
        utime.sleep(duracao)
    buzzer.duty_u16(0)  # Desligar o buzzer

# Função para calcular o score baseado na matriz do jogador e no desenho alvo
def calcular_score(matriz_jogador, desenho_alvo):
    acertos = 0
    total = len(desenho_alvo)
    for (x, y, cor) in desenho_alvo:
        if matriz_jogador[y][x] == cor:
            acertos += 1
    return int((acertos / total) * 100)

#Função Loop aguardando inicio
# Inicialização: apagar a matriz de LEDs e limpar o display OLED
# Inicialização: apagar a matriz de LEDs e limpar o display OLED
apagar_matriz()
oled.fill(0)
oled.text("Aperte o botao A", 0, 0)
oled.text("para comecar", 0, 20)
oled.text("EA801 W", 0, 56)
oled.show()

# Definindo as posições dos quadrados
quadrados_5x5 = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 0), (1, 4),
    (2, 0), (2, 4),
    (3, 0), (3, 4),
    (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)
]

quadrados_3x3 = [
    (1, 1), (1, 2), (1, 3),
    (2, 1), (2, 3),
    (3, 1), (3, 2), (3, 3)
]

quadrados_1x1 = [(2, 2)]

cores = [
    (255, 0, 0),    # Vermelho
    (0, 255, 0),    # Verde
    (0, 0, 255)     # Azul
]

# Ordem de crescimento e diminuição (5x5 -> 3x3 -> 1x1 -> 3x3 -> 5x5)
ordem_quadrados = [quadrados_5x5, quadrados_3x3, quadrados_1x1, quadrados_3x3, quadrados_5x5]
cores_animacao = [cores[0], cores[1], cores[2], cores[1], cores[0]]  # Alternando as cores

# Animação de quadrados piscando até o jogador apertar A
while button_a.value() == 1:  # Enquanto o botão A não for pressionado
    for i in range(len(ordem_quadrados)):
        if button_a.value() == 0:  # Sai imediatamente se o botão for pressionado
            break

        # Apaga tudo antes de acender o próximo
        for j in range(25):
            np[j] = (0, 0, 0)

        # Acende os LEDs nas posições do quadrado atual
        for (x, y) in ordem_quadrados[i]:
            np[y * 5 + x] = cores_animacao[i]
        
        np.write()

        # Adiciona um delay para o efeito de piscar
        utime.sleep(0.5)

# Apaga a matriz antes de iniciar o jogo
apagar_matriz()
# Loop principal
while True:
    
    if button_a.value() == 0:  # Botão A pressionado
        utime.sleep(0.3)  # Debounce
        # Selecionar um desenho aleatório
        desenho_atual = random.choice(desenhos)
        desenhar_desenho(desenho_atual)
        mostrar_mensagem("Atencao ao desenho", 0)
        # Mostrar contagem regressiva de 5 segundos com a mensagem "Atencao! Memorize"
        contagem_regressiva(5)
        # Apagar a matriz de LEDs
        apagar_matriz()
        # Mostrar mensagem "Sua vez" e iniciar o cronômetro
        score = 0
        start_time = utime.ticks_ms()
        mostrar_mensagem("Sua vez", score, 0)

        # Variáveis para o cursor e cores
        x, y = 0, 0
        cores = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 0, 0)]  # Lista de cores com a cor apagada
        cor_atual = 0  # Índice da cor atual (branco)
        matriz_jogador = [[(0, 0, 0) for _ in range(5)] for _ in range(5)]  # Matriz para armazenar as cores dos LEDs

        # Função para atualizar o cursor
        def atualizar_cursor():
            np[LED_MATRIX[y][x]] = (int(cores[cor_atual][0] * 0.5), int(cores[cor_atual][1] * 0.5), int(cores[cor_atual][2] * 0.5))
            np.write()

        # Loop para redesenhar
        while True:
            # Verificar se o botão A foi pressionado para reiniciar
            if button_a.value() == 0:
                utime.sleep(0.3)  # Debounce
                apagar_matriz()  # Apagar a matriz de LEDs ao reiniciar
                oled.fill(0)
                oled.text("Aperte o botao A", 0, 0)
                oled.text("para comecar", 0, 20)
                oled.text("EA801 W", 0, 56)
                oled.show()
                break

            # Ler valores do joystick
            vrx_value = vrx.read_u16()
            vry_value = vry.read_u16()

            # Detectar movimento horizontal (invertido)
            if vrx_value < 20000 and x < 4:
                x += 1  # Mover para a direita
                cor_atual = 0  # Resetar a cor atual para branco
                utime.sleep(0.2)  # Atraso para evitar movimentos rápidos demais
            elif vrx_value > 45000 and x > 0:
                x -= 1  # Mover para a esquerda
                cor_atual = 0  # Resetar a cor atual para branco
                utime.sleep(0.2)  # Atraso para evitar movimentos rápidos demais

            # Detectar movimento vertical
            if vry_value < 20000 and y < 4:
                y += 1  # Mover para baixo
                cor_atual = 0  # Resetar a cor atual para branco
                utime.sleep(0.2)  # Atraso para evitar movimentos rápidos demais
            elif vry_value > 45000 and y > 0:
                y -= 1  # Mover para cima
                cor_atual = 0  # Resetar a cor atual para branco
                utime.sleep(0.2)  # Atraso para evitar movimentos rápidos demais

            # Atualizar a matriz de LEDs com as cores selecionadas pelo jogador
            for i in range(5):
                for j in range(5):
                    np[LED_MATRIX[j][i]] = (int(matriz_jogador[j][i][0] * 0.5), int(matriz_jogador[j][i][1] * 0.5), int(matriz_jogador[j][i][2] * 0.5))

            # Atualizar o cursor
            atualizar_cursor()

            # Verificar se o botão B foi pressionado para mudar a cor
            if button_b.value() == 0:
                utime.sleep(0.3)  # Debounce
                cor_atual = (cor_atual + 1) % len(cores)  # Mudar para a próxima cor
                matriz_jogador[y][x] = cores[cor_atual]  # Atualizar a cor na matriz do jogador

            # Calcular o score baseado na matriz do jogador e no desenho alvo
            score = calcular_score(matriz_jogador, desenho_atual)

            # Calcular o tempo decorrido
            elapsed_time = utime.ticks_diff(utime.ticks_ms(), start_time) / 1000

            # Atualizar a mensagem no display OLED
            oled.fill(0)
            mostrar_mensagem("Sua vez", score, elapsed_time)
            oled.text("Restart press A", 0, 50)  # Adicionar a mensagem de reiniciar
            oled.show()

            # Verificar se o score atingiu 100%
            if score == 100:
                desenhar_desenho(desenho_atual, brilho=0.5)  # Garantir que o desenho final permaneça
                tocar_musica()
                mostrar_mensagem("Parabens!", score, elapsed_time)
                oled.text("Restart press A", 0, 50)  # Adicionar a mensagem de reiniciar
                oled.show()

                # Esperar o jogador pressionar o botão A para reiniciar
                while True:
                    if button_a.value() == 0:
                        utime.sleep(0.3)  # Debounce
                        apagar_matriz()  # Apagar a matriz de LEDs ao reiniciar
                        oled.fill(0)
                        oled.text("Aperte o botao A", 0, 0)
                        oled.text("para comecar", 0, 20)
                        oled.text("EA801 W", 0, 56)
                        oled.show()
                        break
                    utime.sleep(0.1)

                break

            utime.sleep(0.01)  # Atualizar o cronômetro a cada 10 milissegundos

