import openai
from app.config import OPENAI_API_KEY
from app.utils import extract_text_from_pdf

# Inicializa chave da OpenAI
openai.api_key = OPENAI_API_KEY


def chat_with_gpt(prompt):
    """Retorna a resposta completa como string (usa streaming internamente)."""
    response_text = ""
    for chunk in generate_response(prompt):
        response_text += chunk
    return response_text


def generate_response(prompt):
    # Usa a API chat completion com stream do pacote openai
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente abacate que gosta de abacates muito útil."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )

    buffer = ""
    for chunk in resp:
        # cada chunk é um dict com 'choices'
        for choice in chunk.get('choices', []):
            delta = choice.get('delta', {})
            content = delta.get('content')
            if content:
                buffer += content
                if buffer.endswith(('.', '!', '?')):
                    yield buffer
                    buffer = ""
    if buffer:
        yield buffer


def generate_response_stream(prompt):
    # generator reutilizável para streaming por SSE ou chunked responses
    for piece in generate_response(prompt):
        yield piece