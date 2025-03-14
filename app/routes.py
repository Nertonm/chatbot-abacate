from flask import request, jsonify, render_template
from config import UPLOAD_FOLDER
from utils import extract_text_from_pdf
from chat import chat_with_gpt, generate_response_stream
import os

PDF_CONTENT = ""  # Definição da variável global

def init_routes(app):
    global PDF_CONTENT  # Garante que a variável global seja acessada corretamente
        
    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/upload_pdf", methods=["POST"])
    def upload_pdf():
        global PDF_CONTENT  # Permite modificar a variável global
        if "file" not in request.files:
            return jsonify({"message": "Nenhum arquivo enviado."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"message": "Nome do arquivo inválido."}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        PDF_CONTENT = extract_text_from_pdf(file_path)  # Atualizando a variável global

        return jsonify({"message": "PDF recebido e processado!", "text": PDF_CONTENT[:400] + "..."})
    
    @app.route("/ask", methods=["POST"])
    def ask():
        global PDF_CONTENT  # Agora estamos acessando a variável global corretamente
        data = request.json
        question = data.get("question", "").strip()
        if not question:
            return jsonify({"response": "Por favor, faça uma pergunta válida."})
        
        # Se houver conteúdo no PDF e a pergunta mencionar termos relacionados ao documento
        if PDF_CONTENT and any(word in question.lower() for word in ["conteúdo", "pdf", "documento", "arquivo"]):
            return jsonify({"response": f"O PDF carregado contém as seguintes informações: {PDF_CONTENT[:300]}..."})
        
        return generate_response_stream(question)  # Retorna resposta como streaming
    
    @app.route("/stop", methods=["POST"])
    def stop():
        return jsonify({"response": "Processamento interrompido."})
