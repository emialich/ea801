# Guia: Upload de Imagens para o S3 via API Gateway

Este guia mostra como configurar o Amazon API Gateway para receber uploads de imagens (ou PDFs) e enviá-los diretamente para um bucket S3, com suporte a arquivos binários.

---

## Pré-requisitos

- Conta AWS com permissões administrativas
- Bucket S3 já criado
- Ferramenta de testes como Postman ou cURL
- AWS CLI configurado (opcional, para troubleshooting)

---

## 1. Criação da Role IAM para o API Gateway

Crie uma role para o API Gateway com permissão de escrita no S3.

```

aws iam create-role \
--role-name api-gateway-s3-upload \
--assume-role-policy-document '{
"Version": "2012-10-17",
"Statement": [{
"Effect": "Allow",
"Principal": {"Service": "apigateway.amazonaws.com"},
"Action": "sts:AssumeRole"
}]
}'

```

Anexe a seguinte política à role (ajuste o nome do bucket):

```

{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Action": [
"s3:PutObject",
"s3:GetObject"
],
"Resource": "arn:aws:s3:::SEU_BUCKET/*"
}
]
}

```

---

## 2. Estrutura dos Recursos no API Gateway

```

/ (root)
└── {folder} (parâmetro de caminho)
└── {object} (parâmetro de caminho)
├── PUT - Upload handler
└── GET - Download handler

```

---

## 3. Configuração dos Métodos

### PUT (Upload)

- Tipo de integração: AWS Service
- AWS Service: S3
- Método HTTP: PUT
- Caminho do recurso: `{bucket}/{key}`
- Role de execução: ARN da role criada acima

### GET (Download)

- Content-Type: `image/jpeg` ou `application/pdf`
- Adicione os tipos binários: `image/*` e `application/pdf` em **Binary Media Types**

---

## 4. Mapeamento de Parâmetros

| Parâmetro | Origem                       | Destino S3      |
|-----------|------------------------------|-----------------|
| bucket    | method.request.path.folder   | Nome do bucket  |
| key       | method.request.path.object   | Caminho/arquivo |

---

## 5. Deploy da API

```

aws apigateway create-deployment \
--rest-api-id SEU_API_ID \
--stage-name prod

```

---

## 6. Configuração de CORS

Adicione o método OPTIONS e configure o CORS para permitir uploads do navegador:

```

aws apigateway update-integration \
--rest-api-id API_ID \
--resource-id RESOURCE_ID \
--http-method OPTIONS \
--patch-operations op='replace',path='/contentHandling',value='CONVERT_TO_TEXT'

```

---

## 7. Testando os Endpoints

### Upload via cURL

```

curl -X PUT -H "Content-Type: image/jpeg" \
--data-binary "@/caminho/da/imagem.jpg" \
https://API_ID.execute-api.REGIAO.amazonaws.com/prod/BUCKET/arquivo.jpg

```

### Download via Navegador

```

https://API_ID.execute-api.REGIAO.amazonaws.com/prod/BUCKET/arquivo.jpg

```

---

## 8. Troubleshooting

- **403 Forbidden:** Verifique permissões da role e política do bucket
- **400 Bad Request:** Confirme a configuração de tipos binários
- **Erro CORS:** Confirme o método OPTIONS e headers permitidos
- **Timeout:** Regiões do bucket e API Gateway devem ser compatíveis

---

## 9. Boas Práticas

- Habilite cache no API Gateway para downloads frequentes
- Use endpoints VPC para acesso privado ao S3
- Implemente validação de requests
- Defina limites de tamanho de upload (padrão: 10MB)

---

## Referências

- [API Gateway Binary Support](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-payload-encodings.html)
- [Políticas de Bucket S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)


