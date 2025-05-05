# Sistema de Detecção de Movimento com ESP32 e Notificação HTTP

## Descrição

Este projeto implementa um sistema de detecção de movimento baseado no microcontrolador ESP32, utilizando um sensor PIR, LEDs indicadores, um buzzer sonoro e um display LCD I2C. Ao detectar movimento, o sistema emite um alerta visual, sonoro e envia uma notificação HTTP para um endpoint configurado na nuvem, como o Amazon API Gateway.

## Objetivo

O objetivo principal é oferecer uma solução de monitoramento de movimento de baixo custo, eficiente e conectada à internet, com capacidade de alertar remotamente via APIs. A proposta atende aplicações residenciais, educacionais ou experimentais, onde a simplicidade e a conectividade são essenciais.

## Pré-requisitos

* Microcontrolador ESP32
* Sensor PIR (presença)
* Display LCD I2C (endereço 0x27)
* 2 LEDs (azul e vermelho)
* Buzzer piezoelétrico
* Biblioteca `WiFi.h`
* Biblioteca `HTTPClient.h`
* Biblioteca `Wire.h`
* Biblioteca `LiquidCrystal_I2C.h`
* Rede Wi-Fi disponível (sem autenticação via portal cativo)
* Endpoint HTTP funcional (como Amazon API Gateway)

## Instalação

1. **Instale o Arduino IDE**

   * Versão recomendada: 1.8.19 ou superior

2. **Configure o suporte ao ESP32**

   * Vá em `Arquivo > Preferências`, e adicione:

     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   * Em seguida, vá em `Ferramentas > Placa > Gerenciador de Placas` e instale o pacote ESP32

3. **Instale as bibliotecas necessárias**

   * `LiquidCrystal_I2C` (instalável via Gerenciador de Bibliotecas)

4. **Conecte os componentes ao ESP32**:

   * PIR no pino 16
   * LED azul no pino 12
   * LED vermelho no pino 14
   * Buzzer no pino 32
   * Display LCD I2C nos pinos SDA/SCL padrão

5. **Substitua o endpoint na variável `endpoint` do código**

   ```cpp
   const char* endpoint = "https://<seu-endpoint>.amazonaws.com/movimento";
   ```

6. **Compile e envie o código para o ESP32**

## Início Rápido

1. Suba o código no ESP32.
2. Conecte-se à rede Wi-Fi definida em `ssid` e `password`.
3. Ao detectar movimento:

   * O LED vermelho acende
   * O buzzer emite dois bips
   * A mensagem "Movimento detectado" é exibida no LCD
   * Uma requisição HTTP POST é enviada com a mensagem para o endpoint

## Solução de Problemas

* **Erro de conexão Wi-Fi**:

  * Verifique SSID e senha
  * Teste a rede em um celular ou computador

* **LCD não exibe nada**:

  * Confirme o endereço I2C com scanner I2C

* **Buzzer não emite som**:

  * Confirme se está ligado corretamente e se é ativo

* **Endpoint não responde**:

  * Teste manualmente com `curl`
  * Verifique permissões da API Gateway

## Lógica do Sistema e Fluxo de Dados

* O sensor PIR detecta movimento e gera sinal HIGH
* O ESP32 reage ativando o LED vermelho e desativando o azul
* O LCD exibe o alerta textual
* O buzzer emite dois bips alternados com 150 ms
* Um `HTTPClient` realiza um POST com JSON `{ "message": "Movimento detectado!" }`
* Após o envio, o sistema aguarda 10 segundos antes de enviar outro alerta
* Em caso de ausência de movimento, o LED azul é ativado e o LCD é atualizado

## Interação de Componentes

* O sensor PIR atua como entrada principal
* LEDs e buzzer são saídas reativas
* LCD comunica o status ao usuário
* A função `enviarAlertaHTTP()` integra o ESP32 com a nuvem
* Toda a lógica roda no loop principal, com controle de tempo para evitar notificações em excesso

## Custos e Viabilidade Econômica

### Consumo de Energia

* **ESP32**: Consome cerca de 160 mA em modo Wi-Fi ativo (em uso contínuo)
* **Sensor PIR**: Consumo típico de 0.06 W (\~50 µA em standby)
* **LCD I2C e LEDs**: Baixo consumo (<50 mA no total)
* **Buzzer**: Ativado apenas em eventos, consumo desprezível
* A solução pode ser alimentada via fonte USB 5V ou bateria com conversor

### Custos de Componentes (estimativa)

| Componente         | Preço aproximado (BRL) |
| ------------------ | ---------------------- |
| ESP32              | R\$ 35 a R\$ 60        |
| Sensor PIR         | R\$ 5 a R\$ 10         |
| LCD I2C 16x2       | R\$ 15 a R\$ 25        |
| LEDs, buzzer       | R\$ 5                  |
| **Total estimado** | **R\$ 60 a R\$ 100**   |

### Custo de Infraestrutura em Nuvem (AWS)

| Serviço     | Preço (nível gratuito)                         |
| ----------- | ---------------------------------------------- |
| API Gateway | 1 milhão de chamadas/mês grátis por 12 meses   |
| AWS Lambda  | 1 milhão de execuções/mês grátis por 12 meses  |
| Amazon SNS  | 1 milhão de notificações para HTTPS/mês grátis |

> Após o nível gratuito, custos continuam baixos: por exemplo, R\$ 0,0000004 por notificação SNS extra.

Essa arquitetura baseada em eventos é altamente escalável e econômica, sendo ideal para projetos de IoT residenciais ou experimentais com integração em nuvem.

---

Este projeto é modular, educativo e acessível, e pode ser expandido com recursos como controle via app, armazenamento de eventos ou integração com sistemas de segurança maiores.
