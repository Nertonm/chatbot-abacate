from sqlalchemy import Column, Integer, String, Text
from app.extensions import Base


class ChatResponse(Base):
    __tablename__ = 'chat_response'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(500), unique=True, nullable=False)
    answer = Column(Text, nullable=False)