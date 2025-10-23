from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from types import SimpleNamespace
from app.config import SQLALCHEMY_DATABASE_URI, USE_DB


# Sempre expor um Base para que `app.models` possa importar mesmo em modo
# sem banco. Em modo com banco, também será usado para criar tabelas.
Base = declarative_base()


# Modo com DB: cria engine e SessionLocal normalmente.
if USE_DB:
	engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

	def get_db():
		db = SessionLocal()
		try:
			yield db
		finally:
			db.close()

	# Compatibilidade com código Flask antigo que espera `extensions.db.session`.
	# Criamos uma sessão única de compatibilidade para evitar AttributeError em
	# módulos legados que usam `db.session.add(...)`.
	db = SimpleNamespace(session=SessionLocal())

else:
	# Modo sem DB: fornece um DummySession e um armazenamento em memória
	engine = None
	SessionLocal = None

	# armazenamento simples em memória para ChatResponse
	_mem_chat_responses = []

	class DummyQuery:
		def __init__(self, data, model=None):
			self._data = data
			self._filters = {}

		def filter_by(self, **kwargs):
			self._filters.update(kwargs)
			return self

		def first(self):
			for obj in self._data:
				match = True
				for k, v in self._filters.items():
					if getattr(obj, k, None) != v:
						match = False
						break
				if match:
					return obj
			return None

	class DummySession:
		def add(self, obj):
			# Guarda o objeto em memória; atenção: o objeto pode ser uma instância
			# do modelo SQLAlchemy, mas funciona como container de atributos.
			_mem_chat_responses.append(obj)

		def commit(self):
			return None

		def refresh(self, obj):
			return None

		def close(self):
			return None

		def rollback(self):
			return None

		def query(self, model):
			# Suporta apenas ChatResponse para os fluxos atuais
			return DummyQuery(_mem_chat_responses, model)

	def get_db():
		s = DummySession()
		try:
			yield s
		finally:
			s.close()

	# Compatibilidade com código Flask antigo que espera `extensions.db.session`.
	db = SimpleNamespace(session=DummySession())
