import fitz
import openai
import pymysql
from config import OPENAI_API_KEY, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, BOOL

client = openai.Client(api_key=OPENAI_API_KEY)


# Verifica a conexão com o banco de dados
def check_db_connection():
    return False
    
db_connected = check_db_connection()

def extract_text_from_pdf(pdf_path):
    """Lê o conteúdo de um arquivo PDF e retorna o texto extraído."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

# Função para interagir com o ChatGPT
def chat_with_gpt(prompt):
    response_text = ""
    for chunk in generate_response(prompt):
        response_text += chunk
    return response_text

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente abacate que gosta de abacates muito util."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    buffer = ""
    for chunk in response:
        if chunk.choices and hasattr(chunk.choices[0].delta, "content"):
            content = chunk.choices[0].delta.content
            if content:
                buffer += content
                if buffer.endswith(('.', '!', '?')):  # Verifica se a resposta está completa
                    yield buffer
                    buffer = ""
    if buffer:  # Garante que o buffer restante seja enviado
        yield buffer

def generate_response_stream(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente abacate que gosta de abacates muito util."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    buffer = ""
    for chunk in response:
        if chunk.choices and hasattr(chunk.choices[0].delta, "content"):
            content = chunk.choices[0].delta.content
            if content:
                buffer += content
                if buffer.endswith(('.', '!', '?')):  # Verifica se a resposta está completa
                    yield buffer
                    buffer = ""
    if buffer:  # Garante que o buffer restante seja enviado
        yield buffer

