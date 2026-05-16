from flask import Flask, request, jsonify, render_template
import requests
import numpy as np
import os

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_FILE = "embedding.npy"
KNOWLEDGE_BASE = "base_conhecimento.txt"

historico = []

def inicializar_base_conhecimento():
    """Verifica se o arquivo de embedding existe; caso contrário, gera e salva."""
    if os.path.exists(EMBEDDING_FILE):
        print(f"--- Arquivo {EMBEDDING_FILE} encontrado. Carregando...")
        return np.load(EMBEDDING_FILE)
    
    if not os.path.exists(KNOWLEDGE_BASE):
        print("--- Erro: base_conhecimento.txt não encontrada para gerar embeddings.")
        return None

    print(f"--- Gerando novos embeddings a partir de {KNOWLEDGE_BASE}...")
    try:
        with open(KNOWLEDGE_BASE, "r", encoding="utf-8") as f:
            texto = f.read()

        # O Llama 3 consegue gerar o embedding do texto completo ou por partes
        response = requests.post(OLLAMA_EMBED_URL, json={
            "model": "llama3",
            "prompt": texto
        })
        
        embedding_data = response.json()["embedding"]
        embedding_array = np.array(embedding_data)
        
        # Salva o arquivo para não precisar refazer
        np.save(EMBEDDING_FILE, embedding_array)
        print(f"--- Embeddings salvos com sucesso em {EMBEDDING_FILE}")
        return embedding_array
    
    except Exception as e:
        print(f"--- Erro ao processar embeddings: {e}")
        return None

# Carrega os embeddings apenas uma vez na subida da aplicação
embeddings_carregados = inicializar_base_conhecimento()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global historico
   
    data = request.json
    mensagem = data.get("message")

    historico.append(f"Usuário: {mensagem}")
   
    system_prompt = """
    Você é um atendente de uma empresa de manutenção de video game.
    Utilize a base de conhecimento fornecida para responder de forma clara, objetiva e profissional.
    """

    # Aqui você pode incluir lógica adicional para anexar o contexto extraído 
    # da base de conhecimento se desejar faz"er RAG (Busca Semântica).
    prompt = system_prompt + "\n" + "\n".join(historico)

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    resposta = response.json()["response"]
    historico.append(f"Assistente: {resposta}")

    return jsonify({"reply": resposta})

if __name__ == "__main__":
    app.run(debug=True)