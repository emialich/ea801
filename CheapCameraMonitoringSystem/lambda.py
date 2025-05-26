import json
import boto3
import urllib.parse
from datetime import datetime, timezone

sns = boto3.client('sns')
s3 = boto3.client('s3')

SNS_TOPIC_ARN = '***********'
PHOTO_BUCKET = '************'

def lambda_handler(event, context):
    for record in event['Records']:
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        # Obtém horário atual no formato legível
        agora = datetime.now(timezone.utc).astimezone()
        horario_formatado = agora.strftime("%d/%m/%Y às %H:%M:%S")
        
        # Gera a URL temporária da imagem
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': PHOTO_BUCKET, 'Key': key},
            ExpiresIn=3600  # 1 hora
        )
        
        mensagem = (
            f"📸 *Presença detectada em {horario_formatado}*\n\n"
            f"🔗 Acesse a foto aqui:\n{presigned_url}\n\n"
            f"👀 Fique atento!"
        )
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='🚨 Alerta de Presença!',
            Message=mensagem
        )
        
        print("Notificação SNS enviada com sucesso.")

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }
