from machine import Pin, PWM, UART, SoftI2C
import utime
import ssd1306

# UART1: RX = GPIO9, TX = GPIO8
uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))

# Configuração do display OLED SSD1306 (ajuste os pinos se necessário)
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

entrada = Pin(18, Pin.IN)        # Agora usando GPIO18 como entrada
buzzer = PWM(Pin(21))            # Buzzer passivo no GPIO21

# Configuração dos pinos do LED RGB (cátodo comum)
led_r = Pin(13, Pin.OUT)
led_g = Pin(11, Pin.OUT)
led_b = Pin(12, Pin.OUT)

mensagem = "Aguardando..."

def alarme_buzzer(frequencia=2000, tempo=0.1, pausa=0.1):
    buzzer.freq(frequencia)
    buzzer.duty_u16(32768)  # Liga o buzzer (meio ciclo)
    utime.sleep(tempo)
    buzzer.duty_u16(0)      # Desliga o buzzer
    utime.sleep(pausa)

def set_rgb(r, g, b):
    led_r.value(r)
    led_g.value(g)
    led_b.value(b)

while True:
    # Recebe e processa mensagem serial da ESP32-CAM
    if uart.any():
        linha = uart.readline()
        if linha:
            try:
                mensagem = linha.decode().strip()
            except:
                mensagem = "Erro na leitura"
    
    # Exibe mensagem no display
    oled.fill(0)
    oled.text("Ultima mensagem:", 0, 0)
    oled.text(mensagem[:16], 0, 16)  # Mostra até 16 caracteres
    oled.show()
    
    # Lógica do alarme e do LED RGB
    if entrada.value() == 1:
        set_rgb(1, 0, 0)  # Vermelho (alarme ativo)
        alarme_buzzer()
    else:
        set_rgb(0, 0, 1)  # Azul (alarme inativo)
        buzzer.duty_u16(0)
        utime.sleep(0.1)

