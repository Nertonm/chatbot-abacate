"""
Versão Flask (deprecada). Mantida para referência.
"""
from warnings import warn


def deprecated():
    warn('A aplicação foi migrada para FastAPI. Use `uvicorn app.main:app` para executar.')


if __name__ == '__main__':
    deprecated()
