#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ====== CONFIGURAÇÃO DE REDE Wi-Fi ======
const char* ssid = "Wokwi-GUEST";      // Nome da rede Wi-Fi
const char* password = "";             // Senha da rede (vazia no Wokwi)
const char* endpoint = "https://<>.amazonaws.com/movimento"; // Substitua com seu endpoint

// ====== DEFINIÇÃO DOS PINOS ======
const int PIR_PIN = 16;        // Sensor de presença (PIR)
const int LED_AZUL = 12;       // LED azul (sem movimento)
const int LED_VERMELHO = 14;   // LED vermelho (movimento detectado)
const int BUZZER_PIN = 32;     // Buzzer

// ====== INICIALIZAÇÃO DO LCD ======
LiquidCrystal_I2C lcd(0x27, 16, 2); // Endereço I2C 0x27, 16 colunas, 2 linhas

// ====== CONTROLE DE ENVIO ======
unsigned long ultimaDeteccao = 0;
const unsigned long intervaloEnvio = 10000; // 10 segundos entre envios

void setup() {
  // Inicialização de pinos
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_AZUL, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Inicialização Serial
  Serial.begin(115200);

  // Inicialização do LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Sistema iniciado");
  delay(2000);
  lcd.clear();

  // Conexão com Wi-Fi
  Serial.print("Conectando-se ao Wi-Fi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println(" Conectado!");
}

void loop() {
  int movimento = digitalRead(PIR_PIN);

  if (movimento == HIGH) {
    // LED e LCD para presença detectada
    digitalWrite(LED_VERMELHO, HIGH);
    digitalWrite(LED_AZUL, LOW);
    lcd.setCursor(0, 0);
    lcd.print("Movimento        ");
    lcd.setCursor(0, 1);
    lcd.print("detectado!       ");
    Serial.println("Movimento detectado!");

    // Emitir alerta sonoro: padrão bip-bip
    for (int i = 0; i < 2; i++) {
      tone(BUZZER_PIN, 1000); // Frequência de 1000 Hz
      delay(150);             // Duração do bip
      noTone(BUZZER_PIN);
      delay(150);             // Pausa entre bips
    }

    // Envio via HTTP apenas se já passou tempo suficiente
    unsigned long agora = millis();
    if (agora - ultimaDeteccao > intervaloEnvio) {
      enviarAlertaHTTP();
      ultimaDeteccao = agora;
    }

  } else {
    // LED e LCD para ausência de movimento
    digitalWrite(LED_VERMELHO, LOW);
    digitalWrite(LED_AZUL, HIGH);
    lcd.setCursor(0, 0);
    lcd.print("Sem movimento    ");
    lcd.setCursor(0, 1);
    lcd.print("                 ");
    Serial.println("Sem movimento.");
  }

  delay(200);
}

// ====== FUNÇÃO PARA ENVIAR ALERTA VIA HTTP POST ======
void enviarAlertaHTTP() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(endpoint);
    http.addHeader("Content-Type", "application/json");

    // Mensagem simples (sem hora)
    String mensagem = "{\"message\": \"Movimento detectado!\"}";

    int codigoResposta = http.POST(mensagem);
    Serial.print("HTTP POST enviado. Código resposta: ");
    Serial.println(codigoResposta);

    http.end();
  } else {
    Serial.println("Falha na conexão Wi-Fi. Não foi possível enviar o alerta.");
  }
}
