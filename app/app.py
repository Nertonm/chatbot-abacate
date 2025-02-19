from openai import OpenAI
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv() 

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Inicializa o Flask
app = Flask(__name__)

# Banco de dados online no SUPABASE nao mudar nao apagar
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@db.ksxolsmomsdjlrlzzzhe.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Banco de dados online no SUPABASE nao mudar nao apagar

# Inicializa o banco de dados
db = SQLAlchemy(app)

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


@app.route('/add', methods=['POST'])
def add_mensagem():
    data = request.json
    user_message = data.get("user_message")

    print(f"\n🔵 Mensagem do usuário: {user_message}")

    # Verifica no banco `faq` se a pergunta já existe
    faq_entry = Faq.query.filter(Faq.question.ilike(user_message)).first()

    if faq_entry:
        bot_response = faq_entry.answer
        print(f"🟢 Resposta do FAQ encontrada: {bot_response}")
    else:
        # Consulta o ChatGPT caso nao ache a pergunta no banco
        try:
            resposta_completa = ""
            resposta = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": user_message}],
                max_tokens=300,
                temperature=0,
                stream=True)
            
            # Processamento da resposta gerada
            for resposta_stream in resposta:
                texto = resposta_stream.choices[0].delta.content
                if texto:
                    resposta_completa += texto
                    print(texto, end='')

            bot_response=resposta_completa
            # coloca a pergunta no banco
            new_faq = Faq(question=user_message, answer=bot_response)
            db.session.add(new_faq)
            db.session.commit()

        except Exception as e:
            print(f"Erro ao se comunicar com o OpenAI: {e}")
            return jsonify({"message": f"Erro ao obter resposta do ChatGPT: {str(e)}"}), 500

    # armazena no message, que é um historico
    new_message = Message(user_message=user_message, bot_response=bot_response)
    db.session.add(new_message)
    db.session.commit()

    print(f"✅ Interação registrada no banco!\n")
    return jsonify({"message": "Mensagem adicionada!", "bot_response": bot_response})

# Rota para obter todas as mensagens registradas no banco `messages`
@app.route('/mensagens', methods=['GET'])
def get_mensagens():
    messages = Message.query.all()
    mensagens = [{"id": msg.id, "user_message": msg.user_message, "bot_response": msg.bot_response} for msg in messages]
    return jsonify(mensagens)

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
