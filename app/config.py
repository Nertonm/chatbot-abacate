import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
PDF_CONTENT = ""
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://chatbot_user:chatbot_password@db:3306/chatbot_db')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
