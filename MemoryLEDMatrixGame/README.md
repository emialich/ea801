# EA801 - Laboratório de Projetos de Sistemas Embarcados (1S/2025)

Este repositório contém os projetos desenvolvidos ao longo da disciplina **EA801 - Laboratório de Projetos de Sistemas Embarcados**, oferecida no primeiro semestre de 2025.

## Sobre a disciplina

**EA801** tem como foco a metodologia de projeto aplicada ao desenvolvimento de sistemas embarcados. Durante o curso, são abordados temas como:

- Especificação, desenvolvimento e implementação de projetos embarcados
- Protocolos de comunicação
- Revisão de circuitos eletrônicos para interface com atuadores e sensores
- Concorrência entre tarefas
- Expansão de memória
- Princípios de sistemas operacionais em tempo real (RTOS)


## Placa de desenvolvimento: BitDogLab V7

Os projetos desta disciplina utilizam a plataforma **BitDogLab V7**, uma placa didática baseada na **Raspberry Pi Pico H ou W**, desenvolvida no contexto do projeto [Escola 4.0 da Unicamp](https://escola4pontozero.fee.unicamp.br/).

A BitDogLab possui diversos componentes integrados, como:

- **Matriz de LEDs WS2812B 5x5 (Neopixel)** no GPIO7
- **LED RGB** (catodo comum) nos GPIOs 11, 12 e 13
- **3 botões físicos (A, B, C)** nos GPIOs 10, 5 e 6 (com pull-up interno)
- **Joystick analógico KY023** (VRx no GPIO27, VRy no GPIO26, botão no GPIO22)
- **Buzzer passivo** no GPIO21 (via transistor)
- **Display OLED 128x128 via I2C** nos GPIOs 2 (SDA) e 3 (SCL)
- **Microfone com saída analógica** no GPIO28
- **Barras de conexão tipo jacaré**, conectores I2C e IDC para expansão

Mais detalhes técnicos estão disponíveis no [repositório oficial da BitDogLab](https://github.com/Fruett/BitDogLab).

## Estrutura do repositório

```
ea801/MemoryLEDMatrixGame/
        │   ├── README.md                  # Explicação específica do projeto
        │   ├── main.py                    # Código principal do jogo
        │   ├── assets/                    # Imagens, esquemas de ligação, vídeos ou diagramas
        │   │   └── esquema_matriz_leds.png
        │   ├── docs/                      # Documentação técnica complementar 
        │   │   └── relatório_projeto.pdf
        │   └── requirements.txt           # Lista de bibliotecas (se houver)
```


