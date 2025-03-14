import fitz  # PyMuPDF para ler PDFs

def extract_text_from_pdf(pdf_path):
    """Lê o conteúdo de um arquivo PDF e retorna o texto extraído."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text