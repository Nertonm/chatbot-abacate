"""
Este arquivo era a entrada do app Flask. O projeto foi migrado para FastAPI.
Mantenho este arquivo por compatibilidade, mas execute o servidor com:

    uvicorn app.main:app --reload --port 5000

"""
from warnings import warn


def deprecated():
    warn('A aplicação foi migrada para FastAPI. Use `uvicorn app.main:app` para executar.')


if __name__ == '__main__':
    deprecated()