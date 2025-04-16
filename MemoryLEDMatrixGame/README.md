
# Memory LED Matrix Game – Jogo Interativo de Memória com Matriz de LEDs

O Projeto 01 da disciplina Laboratório de Projetos Embarcados (EA801), do curso de Engenharia Elétrica da Universidade Estadual de Campinas (Unicamp), tem como principal objetivo proporcionar aos alunos uma familiarização prática com a placa de desenvolvimento BitDogLab, que é mostrada na figura abaixo.  
A ideia central do projeto é explorar os principais periféricos integrados à placa — como a matriz de LEDs RGB, o joystick, o display OLED, os botões e os buzzer piezo elétricos — por meio da implementação de uma aplicação interativa e lúdica: um Jogo da Memória digital.

![image](https://github.com/user-attachments/assets/2918a612-7af4-4ff2-9a58-c122016b3653)

O **Memory LED Matrix Game** é um jogo eletrônico de memória envolvente que desafia os jogadores a recriar padrões exibidos em uma matriz de LEDs 5x5. Desenvolvido com **MicroPython** em hardware embarcado, ele combina habilidades de memória visual com coordenação motora por meio de uma interface intuitiva baseada em joystick.

O jogo apresenta exibição dinâmica de padrões, controle interativo de LEDs e pontuação em tempo real. Os jogadores devem observar um padrão aleatório, memorizá-lo durante um período de contagem regressiva e depois recriá-lo usando o joystick e um sistema de seleção de cores. O jogo fornece feedback imediato através de um **display OLED** com a pontuação e o tempo decorrido, além de sinais sonoros com um buzzer ao completar corretamente o padrão.

---

## Descrição do projeto 

A aplicação proposta consiste em um Jogo da Memória no qual uma imagem colorida (representada por padrões de LEDs acesos de determinadas cores) é exibida por um curto intervalo de tempo na matriz de LED RGB presente na placa. Após esse intervalo, a imagem é apagada da matriz, e o desafio é que o usuário consiga reproduzir a imagem a partir da própria memória visual.

A interação do usuário com o sistema ocorre por meio de um cursor inicial que surge na posição inferior esquerda da matriz. Esse cursor pode ser movido em todas as direções por meio de um joystick analógico, permitindo ao usuário navegar célula por célula na matriz. Para definir a cor dos LEDs e reconstruir a imagem desejada, o jogador utilizará botões físicos da placa, cada um associado a uma cor específica ou a uma função de alternância de cor.

Enquanto o jogador realiza os movimentos e a tentativa de reconstrução da imagem original, o display OLED da placa entra em ação, exibindo em tempo real informações úteis ao jogador, como:
- Um indicador de pontuação (score) que mostra o número de acertos em relação ao padrão original,
- O número de tentativas restantes (caso o jogo incorpore limite de movimentos),
- O tempo restante para completar o desafio com cronômetro.
- Além disso, ao final de cada tentativa, o sistema verifica automaticamente o grau de similaridade entre a imagem reconstruída pelo usuário e o padrão apresentado inicialmente, e, em caso de sucesso total ou parcial, uma música de vitória é reproduzida via o módulo de buzzer piezoelétrico presente na placa, proporcionando uma resposta sonora ao resultado da jogada.

Este projeto visa, portanto, integrar diversos conceitos fundamentais no desenvolvimento de sistemas embarcados, como:
- Controle e varredura de matriz LED RGB,
- Interação via joystick e botões físicos,
- Processamento de entradas do usuário e lógica de jogo,
- Atualização dinâmica de informações em display OLED,
- Geração de sinais sonoros com o buzzer,
- E a aplicação de boas práticas de programação embarcada utilizando os recursos fornecidos pela placa BitDogLab.

##  Estrutura do Repositório
```
ea801/
└── Memory LED Matrix Game/
    └── main.py           # Lógica principal do jogo, incluindo controle da matriz de LEDs, entrada do usuário e fluxo do jogo
    └── docs.md           # Descrição das principais funções utilizadas
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

## Fluxo de Dados e Diagrama de blocos

O jogo processa a entrada do usuário via joystick e botões, atualiza a exibição na matriz de LEDs e fornece retorno visual e sonoro por meio do display OLED e do buzzer.

```ascii
[Joystick/Botões] -> [Processamento de Entrada] -> [Lógica do Jogo] -> [Matriz de LEDs/OLED/Buzzer]
     ^                                                              |
     |                                                              |
     +--------------------------------------------------------------
```

![image](https://github.com/user-attachments/assets/d9b2447a-b984-469f-9419-e29e59d605ad)

---

## Interações entre Componentes

1. **Camada de Entrada:** O joystick fornece movimentação em X/Y, os botões disparam ações
2. **Lógica do Jogo:** Processa entradas, gerencia o estado do jogo e calcula a pontuação
3. **Camada de Exibição:** Atualiza a matriz de LEDs e o display OLED
4. **Sistema de Feedback:** Mostra pontuação, tempo e emite som de vitória
5. **Gerenciamento de Memória:** Armazena o padrão atual e a recriação feita pelo jogador
6. **Sistema de Temporização:** Gerencia a contagem regressiva e o tempo de execução
7. **Máquina de Estados:** Controla o fluxo entre exibição, memorização e recriação dos padrões

 ## Demonstração

Este vídeo ilustra como configurar e controlar uma matriz de LEDs 5x5 para exibir diferentes formas e padrões com as cores permitidas.​

[![Demonstração de Matriz RGB 5x5](https://img.youtube.com/vi/6ZmRwQnfx24/0.jpg)](https://youtu.be/6ZmRwQnfx24?si=81t3b26qD8APU6OC)

