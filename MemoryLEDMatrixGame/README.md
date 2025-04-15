
# Memory LED Matrix Game – Jogo Interativo de Memória com Matriz de LEDs

O **Memory LED Matrix Game** é um jogo eletrônico de memória envolvente que desafia os jogadores a recriar padrões exibidos em uma matriz de LEDs 5x5. Desenvolvido com **MicroPython** em hardware embarcado, ele combina habilidades de memória visual com coordenação motora por meio de uma interface intuitiva baseada em joystick.

O jogo apresenta exibição dinâmica de padrões, controle interativo de LEDs e pontuação em tempo real. Os jogadores devem observar um padrão aleatório, memorizá-lo durante um período de contagem regressiva e depois recriá-lo usando o joystick e um sistema de seleção de cores. O jogo fornece feedback imediato através de um **display OLED** com a pontuação e o tempo decorrido, além de sinais sonoros com um buzzer ao completar corretamente o padrão.

---

##  Estrutura do Repositório
```
ea801/
└── Memory LED Matrix Game/
    └── main.py           # Lógica principal do jogo, incluindo controle da matriz de LEDs, entrada do usuário e fluxo do jogo
```

---

##  Instruções de Uso

###  Pré-requisitos
- Placa microcontroladora compatível com MicroPython
- Componentes de hardware:
  * Matriz de LEDs WS2812B 5x5
  * Display OLED SSD1306 (128x64)
  * Joystick analógico
  * 2 botões de pressão
  * Buzzer (sinalizador sonoro)
  * Ligações necessárias:
    - Matriz de LEDs: Pino 7
    - Display OLED: SCL no pino 15, SDA no pino 14
    - Joystick: VRX no pino 27, VRY no pino 26
    - Botão A: Pino 5
    - Botão B: Pino 6
    - Buzzer: Pino 21

---

###  Instalação

1. Grave o MicroPython na sua placa microcontroladora
2. Copie o arquivo `main.py` para o diretório raiz da placa
3. Instale as bibliotecas necessárias:
```python
import machine
import ssd1306
import neopixel
```

---

###  Início Rápido

1. Ligue o dispositivo  
2. Pressione o Botão A para iniciar o jogo  
3. Observe o padrão mostrado na matriz de LEDs durante a contagem regressiva de 5 segundos  
4. Use o joystick para mover o cursor pela matriz  
5. Pressione o Botão B para alternar entre as cores disponíveis  
6. Recrie o padrão que você memorizou  
7. A pontuação e o tempo serão exibidos no display OLED  

---

###  Exemplo de Criação de Padrões
```python
# Mova o cursor com o joystick
# Pressione o Botão B para alternar entre as cores:
# - Branco (255, 255, 255)
# - Vermelho (255, 0, 0)
# - Verde (0, 255, 0)
# - Azul (0, 0, 255)
# - Amarelo (255, 255, 0)
# - Apagar (0, 0, 0)
```

---

###  Solução de Problemas

**1. Matriz de LEDs não responde**
- Verifique a conexão no Pino 7
- Confirme se a fonte de alimentação fornece 5V suficientes
- Reinicie o dispositivo

**2. Joystick não funciona**
- Verifique as conexões ADC nos pinos 26 e 27
- Calibre o joystick no código, se necessário
- Limiares padrão: abaixo de 20000 e acima de 45000

**3. Problemas com o display OLED**
- Verifique as conexões I2C (SCL: pino 15, SDA: pino 14)
- Confirme o endereço I2C correto (ex: 0x3C)
- Verifique a fonte de alimentação

---

## Fluxo de Dados

O jogo processa a entrada do usuário via joystick e botões, atualiza a exibição na matriz de LEDs e fornece retorno visual e sonoro por meio do display OLED e do buzzer.

```ascii
[Joystick/Botões] -> [Processamento de Entrada] -> [Lógica do Jogo] -> [Matriz de LEDs/OLED/Buzzer]
     ^                                                              |
     |                                                              |
     +--------------------------------------------------------------
```

---

## Interações entre Componentes

1. **Camada de Entrada:** O joystick fornece movimentação em X/Y, os botões disparam ações
2. **Lógica do Jogo:** Processa entradas, gerencia o estado do jogo e calcula a pontuação
3. **Camada de Exibição:** Atualiza a matriz de LEDs e o display OLED
4. **Sistema de Feedback:** Mostra pontuação, tempo e emite som de vitória
5. **Gerenciamento de Memória:** Armazena o padrão atual e a recriação feita pelo jogador
6. **Sistema de Temporização:** Gerencia a contagem regressiva e o tempo de execução
7. **Máquina de Estados:** Controla o fluxo entre exibição, memorização e recriação dos padrões
