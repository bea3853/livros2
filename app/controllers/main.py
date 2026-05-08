from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, Livro, init_db
from pydantic import BaseModel

app = FastAPI()

# Cria as tabelas assim que a API inicia
init_db()

class LivroSchema(BaseModel):
    titulo: str
    autor: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/livros")
def listar_livros(db: Session = Depends(get_db)):
    return db.query(Livro).all()

@app.post("/livros")
def criar_livro(livro: LivroSchema, db: Session = Depends(get_db)):
    novo_livro = Livro(titulo=livro.titulo, autor=livro.autor)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro