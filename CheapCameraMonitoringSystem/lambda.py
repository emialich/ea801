import json
import boto3
from datetime import datetime

# Substitua pelo ARN do seu tópico SNS
TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:meu-topico-sns'

sns = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Se vier do API Gateway, o corpo é uma string JSON
        body = json.loads(event.get('body', '{}'))
        mensagem_base = body.get('message', 'Movimento detectado!')

        # Adiciona data e hora UTC no formato ISO 8601
        agora = datetime.utcnow().isoformat()
        mensagem_completa = f"🔔 ALERTA DE MOVIMENTO\n\n{mensagem_base}\nHorário: {agora} UTC"

        # Publica no SNS
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Movimento Detectado no ESP32",
            Message=mensagem_completa
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"success": True, "message": "Alerta enviado ao SNS"})
        }

    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"success": False, "error": str(e)})
        }
