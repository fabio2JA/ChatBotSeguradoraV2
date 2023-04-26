# OCR - SEGURADORA

## Versão: beta;

#### Features implementadas: reconhecimentos de pdfs e imagens, sistema de filas sem o uso de um broker, api para gerenciar o sistema;
#### Features para serem implementadas: IA para reconhecimento de angulo da imagem, IA para extração somente dos campos desejados, Cobertura de testes automatizados, Redesign do front-end da api;

## Como rodar;

### Para rodar um docker container:
#### ------ ```bash docker build -t app . ```
#### ------ ```bash docker run -p 0000:8000 app  ```

### Para rodar na maquina;

#### ------ ```bash Instale o python 3.10.4 ```
#### ------ ```bash pip install virtualenv ```
#### ------ ```bash virtualenv venv ```
#### ------ ```bash windows> venv/Scripts/activate unix> venv/bin/activate ```
#### ------ ```bash sudo apt-get update ```
#### ------ ```bash sudo apt-get install -y libglu1-mesa-dev poppler-utils ```
#### ------ ```bash pip install django python-dotenv paddlepaddle==2.4.2 paddleocr pdf2image mysqlclient django-cors-headers ```
#### ------ ```bash python manage.py runserver 0.0.0.0:8000 ```

## Como usar;

#### Depois de iniciar o sistema para porta 8000
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_15.png)

#### Escolha entre reconhecer uma cnh ou um documento de carro
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_16.png)

#### Faça o upload da imagem e clique em reconhecer imagem
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_17.png)

#### Aguarde ate a finalizacao do reconhecimento
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_18.png)

#### Se o reconhecimento foi bem sucedido volte a pagina principal, se não tente usar outra imagem
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_19.png)

#### Abra o dashboard do admin
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_20.png)

#### Navege ate motoristas e Escolha o tipo que você selecinou para o reconhecimento
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_21.png)

#### Ira aparecer uma lista de documentos, clique no seu documento
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_22.png)

#### Aqui voce editar e deletar um documento
![](https://github.com/fabio2JA/ChatBotSeguradoraV1/blob/main/OCR/ocr-ai/imagens/Screenshot_23.png)
