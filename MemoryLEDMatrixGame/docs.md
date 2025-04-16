# 📄 Documentação Técnica - Funções e Código

Este documento descreve as principais seções do código e suas respectivas funcionalidades, focando exclusivamente na implementação do jogo de memória em MicroPython.

## 📦 Importações e Inicializações

```python
from machine import Pin, SoftI2C, ADC, PWM
import utime
import ssd1306
import neopixel
import random
```
Essas bibliotecas controlam os periféricos: pinos GPIO, comunicação I2C, controle de LEDs e som.

## 📺 Display OLED

```python
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
```
Inicializa a comunicação com o display OLED SSD1306 via I2C.

## 💡 Matriz de LEDs WS2812B

```python
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)
```
Define uma matriz de 5x5 LEDs (25 LEDs no total), mapeada para facilitar a visualização e controle dos pixels.

## 🎮 Controles (Joystick e Botões)

```python
vrx = ADC(Pin(27))  # Movimento horizontal
vry = ADC(Pin(26))  # Movimento vertical
button_a = Pin(5, Pin.IN, Pin.PULL_UP)  # Botão A (iniciar)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)  # Botão B (mudar cor)
```
O joystick é lido por ADC e os botões usam resistores de pull-up internos.

## 🔊 Buzzer

```python
buzzer = PWM(Pin(21))
```

Usado para reproduzir sons durante o jogo.

---

## 🧩 Funções Principais

### `desenhar_desenho(desenho, brilho=0.5)`
Acende os LEDs de acordo com um padrão predefinido. Cada ponto é uma tupla `(x, y, cor)`.

### `mostrar_mensagem(mensagem, score=None, tempo=None)`
Mostra mensagens no display OLED. Pode exibir também a pontuação e o tempo.

### `contagem_regressiva(segundos)`
Mostra uma contagem regressiva no display OLED antes de exibir o padrão a ser memorizado.

### `apagar_matriz()`
Apaga todos os LEDs da matriz.

### `tocar_musica()`
Reproduz uma sequência de notas no buzzer.

### `calcular_score(matriz_jogador, desenho_alvo)`
Compara a entrada do jogador com o desenho original e retorna uma pontuação percentual de acertos.