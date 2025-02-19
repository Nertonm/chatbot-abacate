from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Configuração da conexão com o MySQL
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_DATABASE')
}

# Função para conectar ao banco de dados MySQL
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/add_message', methods=['POST'])
def add_message():
    data = request.get_json()
    user_message = data.get('message')

    # Aqui você pode integrar com o ChatGPT (OpenAI)
    bot_response = get_bot_response(user_message)

    # Conectar ao banco de dados e salvar a mensagem
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (user_message, bot_response) VALUES (%s, %s)', 
                   (user_message, bot_response))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'user_message': user_message, 'bot_response': bot_response})

# Função para obter resposta do ChatGPT (simulada)
def get_bot_response(user_message):
    # Aqui você pode integrar com a API do ChatGPT da OpenAI
    return "Resposta do bot para: " + user_message

if __name__ == "__main__":
    app.run(debug=True)
