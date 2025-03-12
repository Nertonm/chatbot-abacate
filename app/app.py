from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os

app = Flask(__name__)

# Configuração da conexão com o MySQL
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "DB_ROOT_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "mysql")  # Nome do serviço no Docker Compose
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "DB_NAME")

DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criando a conexão diretamente com create_engine
engine = create_engine(DATABASE_URI)

# Inicializa o SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Testa a conexão
try:
    with engine.connect() as connection:
        print("✅ Conexão com MySQL bem-sucedida!")
except Exception as e:
    print(f"❌ Erro ao conectar ao MySQL: {e}")

# Modelo de Dados
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

# Criar tabelas no banco (se não existirem)
with app.app_context():
    db.create_all()


# Modelo de Dados para a Tabela 'messages'
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

# Modelo de Dados para a Tabela 'faq'
class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

# Criação das Tabelas no Banco (caso não existam)
with app.app_context():
    db.create_all()