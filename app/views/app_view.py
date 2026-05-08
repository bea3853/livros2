import streamlit as st
import requests
import os

# st.set_page_config(page_title="Biblioteca Digital", page_icon="-book-")

# LOCAL: http://127.0.0.1:8000/livros
# PRODUÇÃO: https://seu-projeto.onrender.com/livros
# API_URL = os.getenv("https://api-livros-bea.onrender.com", "http://127.0.0.1:8000/livros")

# ---------------------

st.set_page_config(page_title="Biblioteca Digital")

# --- A VERIFICAÇÃO ACONTECE AQUI ---
# 1. Ele tenta ler a chave "API_URL" dos Secrets do Streamlit (Nuvem)
# 2. Se não existir, ele tenta ler das variáveis de ambiente do Windows/Linux
# 3. Se ainda assim não achar, ele usa o localhost (para o seu teste no VS Code)
API_URL = st.secrets.get("https://api-livros-bea.onrender.com", os.getenv("https://api-livros-bea.onrender.com", "http://127.0.0.1:8000/livros"))

# st.title("Gestor de Livros (MVC)")

# Verificação visual para você saber qual URL o app está usando
# st.write(f"Conectado em: {API_URL}") # Descomente para testar

# --------------------
st.title(" Gestor de Livros (MVC)")

with st.sidebar:
    st.header("Novo Livro")
    titulo = st.text_input("Título")
    autor = st.text_input("Autor")
    if st.button("Cadastrar"):
        if titulo and autor:
            res = requests.post(API_URL, json={"titulo": titulo, "autor": autor})
            if res.status_code == 200:
                st.success("Livro salvo!")
            else:
                st.error("Erro na API")

st.subheader("Livros Disponíveis")
if st.button("Atualizar Lista"):
    try:
        livros = requests.get(API_URL).json()
        for l in livros:
            st.info(f"**{l['titulo']}** | Autor: {l['autor']}")
    except:
        st.error("Não foi possível conectar à API. Verifique se o servidor está ligado.")
