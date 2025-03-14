# Chatbot Abacate  

Chatbot Abacate é um projeto integrador desenvolvido no IFCE. Trata-se de uma aplicação de chatbot que interage com os usuários utilizando o modelo GPT-3.5-turbo da OpenAI. A aplicação está implantada usando Dokku e pode ser acessada em:  

🔗 [http://chatbot-abacate.paas.capacitabrasil.ifce.edu.br/](http://chatbot-abacate.paas.capacitabrasil.ifce.edu.br/)  

## Estrutura do Projeto  

```
chatbot-abacate/  
├── app/  
│   ├── __init__.py  
│   ├── app.py  
│   ├── chat.py  
│   ├── config.py  
│   ├── models.py  
│   ├── routes.py  
│   ├── utils.py  
│   ├── templates/  
│   │   └── index.html  
│   ├── static/  
│   └── instance/  
├── uploads/  
├── Dockerfile
├── docker-compose.yml
├── requirements.txt  
├── init_db.sql  
├── init_db.sh  
└── .env  
```  

## Configuração e Instalação  

### Pré-requisitos  

- Docker  

### Variáveis de Ambiente  

Crie um arquivo `.env` no diretório raiz do projeto e adicione as seguintes variáveis de ambiente:  

```
OPENAI_API_KEY=your_openai_api_key  
DB_HOST=your_database_host  
DB_USER=your_database_user  
DB_PASSWORD=your_database_password  
DB_NAME=your_database_name  
BOOL=your_boolean_value  
DATABASE_URL=mysql+pymysql://chatbot_user:chatbot_password@db:3306/chatbot_db  
```  

Rodar o Projeto com Docker Compose

Para iniciar a aplicação utilizando Docker Compose, execute os seguintes comandos:
```
git clone https://github.com/seu-usuario/chatbot-abacate.git
cd chatbot-abacate
cp .env.example .env  # Edite o .env conforme necessário
docker-compose up --build -d
```
Isso irá:

Construir e iniciar os containers do chatbot e do banco de dados.

Rodar as migrações para configurar o banco de dados.
