#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include "time.h"

// ======= Configurações da câmera (modelo AI Thinker) =======
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

// ======= Credenciais de Wi-Fi e Endpoint da API =======
const char* ssid = "******";
const char* password = "*****";

// Substitua pela base da sua API
const char* base_url = "****";  //

// ======= GPIO do flash (LED embutido) =======
#define FLASH_GPIO 4

// ======= GPIOs do ultrassônico =======
#define TRIG_PIN 14
#define ECHO_PIN 15

// ======= GPIO de saída para alarme =======
#define OUTPUT_ALARM_GPIO 12

// ======= Parâmetros do ultrassônico =======
#define DISTANCIA_LIMITE_CM 5
unsigned long delayFoto = 30000; // 15 segundos (configurável)
unsigned long ultimaFotoMillis = 0;

// ======= NTP =======
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -3 * 3600; // Ajuste para GMT-3
const int   daylightOffset_sec = 0;

// ======= Função para piscar o flash =======
void blinkFlash(int pin, int duration_ms) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);
  delay(duration_ms);
  digitalWrite(pin, LOW);
}

// ======= Função para conectar ao Wi-Fi =======
void connectWiFi() {
  Serial.println("Iniciando conexão WiFi...");
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("\nWiFi conectado com sucesso!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
  blinkFlash(FLASH_GPIO, 200);
}

// ======= Função para obter data/hora =======
String getDateTimeString() {
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    return "no_time";
  }
  char buffer[32];
  strftime(buffer, sizeof(buffer), "%Y%m%d_%H%M%S", &timeinfo);
  return String(buffer);
}

// ======= Função para medir distância (em cm) =======
float medirDistanciaCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracao = pulseIn(ECHO_PIN, HIGH, 30000); // timeout 30ms
  if (duracao == 0) return -1; // Sem leitura

  float distancia = (duracao * 0.0343) / 2.0;
  return distancia;
}

// ======= Função para capturar e enviar a foto =======
void captureAndSendPhoto(String datetime) {

  blinkFlash(FLASH_GPIO, 200);
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Erro ao capturar foto.");
    return;
  }

  Serial.println("Foto capturada");
  

  if (WiFi.status() == WL_CONNECTED) {
    String nome_arquivo = "/foto_" + datetime + ".jpg";
    String full_url = String(base_url) + nome_arquivo;
    //Serial.print("S: ");
    //Serial.println(full_url);

    HTTPClient http;
    http.begin(full_url);
    http.addHeader("Content-Type", "image/jpeg");

    int httpResponseCode = http.sendRequest("PUT", fb->buf, fb->len);
    Serial.printf("HTTP: %d\n", httpResponseCode);

    String resposta = http.getString();
    //Serial.println("Resposta da API:");
    //Serial.println(resposta);

    //Serial.print("Foto tirada em: ");
    //Serial.println(datetime);
    //Serial.print("Nome do arquivo: ");
    //Serial.println(nome_arquivo);
    esp_camera_fb_return(fb);
    http.end();
  } else {
    Serial.println("Erro: Wi-Fi desconectado.");
  }

  esp_camera_fb_return(fb);
}

// ======= Setup da ESP32-CAM =======
void setup() {
  Serial.begin(115200); // Serial0: TX=GPIO3, RX=GPIO1
  Serial.println("Inicializando ESP32-CAM...");

  // Configuração dos pinos do ultrassônico
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Configuração do pino de saída para alarme
  pinMode(OUTPUT_ALARM_GPIO, OUTPUT);
  digitalWrite(OUTPUT_ALARM_GPIO, LOW); // Inicialmente desligado

  // Configuração da câmera (padrão AI Thinker)
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.fb_count = 1;
  if(psramFound()){
    config.frame_size = FRAMESIZE_VGA;
    config.jpeg_quality = 10;
    config.fb_count = 1;
  } else {
    config.frame_size = FRAMESIZE_CIF;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Erro ao iniciar a câmera: 0x%x", err);
    return;
  }

  connectWiFi();

  // Inicializa NTP
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("Aguardando sincronização NTP...");
  struct tm timeinfo;
  while(!getLocalTime(&timeinfo)){
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nHorário sincronizado!");
  //ultimaFotoMillis = millis() - delayFoto; // Permite foto logo no início
}

// ======= Loop principal =======
void loop() {
  float distancia = medirDistanciaCM();
  //Serial.print("Distância medida: ");
  if (distancia > 0) {
    //Serial.print(distancia, 1);
    //Serial.println(" cm");
    // Transmite apenas a distância pela UART (pinos 1/3)
    Serial.print("Dist:");
    Serial.println(distancia, 2); // Exemplo: "DISTANCIA_UART:9.87"
  } else {
    Serial.println("Sem leitura");
  }

  unsigned long agora = millis();
  if (distancia > 0 && distancia < DISTANCIA_LIMITE_CM) {
    digitalWrite(OUTPUT_ALARM_GPIO, HIGH); // Mantém GPIO12 em alto enquanto presença
    if (agora - ultimaFotoMillis >= delayFoto) {
      String datetime = getDateTimeString();
      //Serial.println(">>> PRESENÇA DETECTADA: Menor que 10 cm <<<");
      captureAndSendPhoto(datetime);
      ultimaFotoMillis = agora;
    } else {
      //Serial.print("Aguardando próximo envio em ");
      //Serial.print((delayFoto - (agora - ultimaFotoMillis)) / 1000);
      //Serial.println(" segundos...");
    }
  } else {
    digitalWrite(OUTPUT_ALARM_GPIO, LOW); // Desliga GPIO12 se não houver presença
  }
  delay(200); // Pequeno delay para evitar leituras excessivas
}
