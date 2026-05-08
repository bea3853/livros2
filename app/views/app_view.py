import streamlit as st
import requests
import os

# Configuração da página (deve ser a primeira coisa do Streamlit)
st.set_page_config(page_title="Biblioteca Digital")

# --- A VERIFICAÇÃO CORRETA ---
# O segredo é usar um nome simples ("API_URL"). 
# O link real você vai cadastrar lá no painel do Streamlit Cloud.
API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://127.0.0.1:8000/livros"))

st.title("Gestor de Livros (MVC)")

# Sidebar para cadastro
with st.sidebar:
    st.header("Novo Livro")
    titulo = st.text_input("Título")
    autor = st.text_input("Autor")
    
    if st.button("Cadastrar"):
        if titulo and autor:
            try:
                res = requests.post(API_URL, json={"titulo": titulo, "autor": autor})
                if res.status_code == 200:
                    st.success("Livro salvo!")
                else:
                    st.error(f"Erro na API: {res.status_code}")
            except Exception as e:
                st.error("Erro de conexão. A API está online?")
        else:
            st.warning("Preencha todos os campos.")

# Listagem de livros
st.subheader("Livros Disponíveis")

if st.button("Atualizar Lista"):
    try:
        # Faz a requisição para a URL que estiver na variável API_URL
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            livros = response.json()
            if not livros:
                st.info("Nenhum livro encontrado.")
            for l in livros:
                st.info(f"**{l['titulo']}** | Autor: {l['autor']}")
        else:
            st.error("A API retornou um erro ao buscar a lista.")
            
    except Exception as e:
        st.error(f"Não foi possível conectar à API em: {API_URL}")

# Dica para debug (pode apagar depois)
with st.expander("Verificar Conexão"):
    st.write(f"Endereço atual da API: `{API_URL}`")
