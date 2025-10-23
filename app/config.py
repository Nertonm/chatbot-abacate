import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
PDF_CONTENT = ""

# Prefer DATABASE_URL; senão, constrói a partir de DB_* (útil no Docker Compose)
database_url = os.getenv('DATABASE_URL')
if not database_url:
	db_user = os.getenv('DB_USER', 'chatbot_user')
	db_password = os.getenv('DB_PASSWORD', 'chatbot_password')
	db_host = os.getenv('DB_HOST', 'db')
	db_port = os.getenv('DB_PORT', '3306')
	db_name = os.getenv('DB_NAME', 'chatbot_db')
	database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

SQLALCHEMY_DATABASE_URI = database_url
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Permite executar a aplicação sem conexão com banco de dados externo.
# Defina DISABLE_DB=1 ou DISABLE_DB=true para ativar o modo sem-banco.
DISABLE_DB = str(os.getenv('DISABLE_DB', '0')).lower() in ('1', 'true', 'yes')
USE_DB = not DISABLE_DB
