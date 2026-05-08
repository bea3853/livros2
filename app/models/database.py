import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Se estiver no Render, ele usa a DATABASE_URL do Neon. 
# Se estiver no seu PC, ele cria o livros.db local.
SQLALCHEMY_DATABASE_URL = os.getenv('postgresql://neondb_owner:npg_Ian3Oow5rFgP@ep-late-cherry-aq0uxpgf-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require', "sqlite:///./livros.db")

# Ajuste para compatibilidade com PostgreSQL no Render
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Livro(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)