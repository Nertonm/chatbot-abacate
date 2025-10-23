from fastapi import FastAPI, UploadFile, File, Form, Body, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from app.extensions import SessionLocal, engine, Base
import time
import os
import pymysql
from sqlalchemy.exc import OperationalError
from app.models import ChatResponse
from app.utils import extract_text_from_pdf
from app import chat
import shutil
import os



app = FastAPI(title="Chatbot Abacate")


@app.on_event("startup")
def startup_event():
    """Tentativa de conexão com o banco e criação das tabelas com retries.

    Em ambientes com Docker Compose o banco pode demorar para ficar pronto;
    aqui fazemos várias tentativas antes de falhar para evitar crash loops.
    """
    # more robust connection check using pymysql for clearer diagnostics
    retries = int(os.getenv('DB_STARTUP_RETRIES', '20'))
    delay = int(os.getenv('DB_STARTUP_DELAY', '3'))
    db_host = os.getenv('DB_HOST', 'db')
    db_port = int(os.getenv('DB_PORT', '3306'))
    db_user = os.getenv('DB_USER', os.getenv('MYSQL_USER', 'chatbot_user'))
    db_pass = os.getenv('DB_PASSWORD', os.getenv('MYSQL_PASSWORD', 'chatbot_password'))
    db_name = os.getenv('DB_NAME', 'chatbot_db')

    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempting DB auth connection to {db_user}@{db_host}:{db_port}/{db_name} (attempt {attempt}/{retries})")
            conn = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_pass, database=db_name, connect_timeout=5)
            conn.close()
            # If auth successful, create tables via SQLAlchemy
            Base.metadata.create_all(bind=engine)
            print("DB connected and tables created successfully")
            return
        except Exception as e:
            last_exc = e
            print(f"DB connection failed (attempt {attempt}/{retries}): {e}")
            time.sleep(delay)
    # If here, could not connect
    raise RuntimeError(f"Could not connect to DB after {retries} retries. Last error: {last_exc}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', response_class=HTMLResponse)
def index():
    html_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(f.read())


@app.post('/upload_pdf')
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Apenas arquivos PDF são aceitos')
    dest = os.path.join('uploads', file.filename)
    with open(dest, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = extract_text_from_pdf(dest)
    return {'message': 'PDF recebido e processado!', 'text': text[:400] + '...'}


@app.post('/ask')
async def ask(request: Request, question_form: str = Form(None), payload: dict = Body(None), db=Depends(get_db)):
    """Accept JSON or form-encoded requests. This handler is tolerant to both legacy form posts and
    modern JSON fetch requests.
    """
    q = ''
    # Try to read JSON body first (if any)
    try:
        if request.headers.get('content-type', '').startswith('application/json'):
            data = await request.json()
            if isinstance(data, dict) and 'question' in data:
                q = str(data.get('question', '')).strip()
    except Exception:
        # ignore JSON parsing errors; fallback to other sources
        q = ''

    # Fallback to form field if JSON not provided
    if not q and question_form:
        q = question_form.strip()

    # Fallback to Body param (kept for backward compat)
    if not q and payload and isinstance(payload, dict):
        q = str(payload.get('question', '')).strip()

    if not q:
        raise HTTPException(status_code=400, detail='Pergunta inválida')
    existing = db.query(ChatResponse).filter_by(question=q).first()
    if existing:
        return {'response': existing.answer}

    # Gera resposta e persiste
    answer = chat.chat_with_gpt(q)
    new = ChatResponse(question=q, answer=answer)
    db.add(new)
    db.commit()
    db.refresh(new)
    return {'response': answer}


@app.post('/stop')
def stop():
    return {'response': 'Processamento interrompido.'}
