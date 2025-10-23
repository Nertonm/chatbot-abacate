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
cp .env.exemple .env  # Edite o .env conforme necessário
docker-compose up --build -d
```
Isso irá:

Construir e iniciar os containers do chatbot e do banco de dados.

Rodar as migrações para configurar o banco de dados.

## Executando localmente (sem Docker)

1. Crie e ative um ambiente virtual (Python 3.8+ recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copie variáveis de ambiente e defina sua chave OpenAI em `.env` ou exporte no shell:

```bash
cp .env.example .env
export OPENAI_API_KEY=sk-...
```

3. Crie o banco de dados localmente (ou configure `DATABASE_URL` no `.env`) e rode a aplicação:

```bash
# Rodar localmente com uvicorn
uvicorn app.main:app --reload --port 5000
```

## Notas sobre Docker

O `docker-compose` agora inclui um healthcheck para o serviço `db`. Se o container `web` falhar logo na inicialização, verifique os logs do banco e do web com:

```bash
docker-compose logs -f db
docker-compose logs -f web
docker-compose ps
```

O `web` usa política `restart: on-failure` para tentar reiniciar caso o banco ainda não esteja pronto.

Importante: dentro do Docker Compose o host do banco é o nome do serviço (`db`). Para evitar confusão, você pode:

- Definir `DB_HOST=db` no arquivo `.env` antes de rodar o `docker-compose`.
- Ou exportar `DB_HOST=db` no ambiente antes de executar o compose.

Exemplo (build + start):

```bash
docker-compose build --pull --no-cache
docker-compose up --remove-orphans --force-recreate
```

Para ver logs em tempo real:

```bash
docker-compose logs -f web
```
