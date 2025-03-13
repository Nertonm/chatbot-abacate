import fitz  # PyMuPDF para ler PDFs
import openai
from flask import Flask, request, jsonify, render_template, Response
import threading, os

# Configuração da API OpenAI
client = openai.OpenAI(api_key="")

app = Flask(__name__)

stop_event = threading.Event()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

pdf_content = ""  # Variável global para armazenar o texto do PDF

# Rota para carregar a página HTML
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    global pdf_content  # Usa a variável global para armazenar o texto extraído

    if "file" not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "Nome do arquivo inválido."}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extrai texto do PDF e armazena na variável global
    pdf_content = extract_text_from_pdf(file_path)

    return jsonify({"message": "PDF recebido e processado!", "text": pdf_content[:200] + "..."})


def extract_text_from_pdf(pdf_path):
    """Lê o conteúdo de um arquivo PDF e retorna o texto extraído."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

# Função para interagir com o ChatGPT
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Você é um assistente útil."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def generate_response_stream(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in response:
        if chunk.choices and hasattr(chunk.choices[0].delta, "content"):
            content = chunk.choices[0].delta.content
            if content:
                yield f'{{"response": "{content}"}}\n'


@app.route("/ask", methods=["POST"])
def ask():
    global pdf_content  # Acessa o conteúdo do PDF carregado
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"response": "Por favor, faça uma pergunta válida."})

    if pdf_content:
        return jsonify({"response": f"O PDF carregado contém as seguintes informações: {pdf_content[:300]}..."})
    else:
        # Se não há PDF, chama o ChatGPT normalmente
        resposta_chatgpt = chat_with_gpt(question)
        return jsonify({"response": resposta_chatgpt})
    
@app.route("/stop", methods=["POST"])
def stop():
    global stop_event
    stop_event.set()
    return jsonify({"response": "Processamento interrompido."})

if __name__ == "__main__":
    app.run(debug=True)
