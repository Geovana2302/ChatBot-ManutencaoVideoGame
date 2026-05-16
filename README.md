# 🎮 Console Repair AI - Suporte Técnico Inteligente

Este projeto consiste em um ecossistema de atendimento automatizado voltado para o diagnóstico e manutenção de consoles de videogame (PlayStation, Xbox e Nintendo Switch). A aplicação utiliza uma arquitetura **RAG (Retrieval-Augmented Generation)** para buscar soluções em uma base de conhecimento local e integra-se ao **Dialogflow ES**, permitindo o processamento de linguagem natural e canais de mensageria omnichannels.

---

## 🧠 Arquitetura e Funcionamento do Projeto

O fluxo de processamento de mensagens segue uma divisão clara de responsabilidades:

1. **Camada de Interação e NLP (Dialogflow ES):** O usuário envia uma mensagem (via webchat ou mensageria). O Dialogflow interpreta a intenção do usuário através das *Training Phrases* da Intent `suporte.manutencao`.
2. **Tunelamento Seguro (Ngrok):** O Dialogflow encaminha a requisição HTTP POST para a URL pública gerada pelo Ngrok, que faz o redirecionamento seguro para o servidor local na porta `5000`.
3. **Regras de Negócio e Webhook (Flask):** O endpoint `/webhook` em `app.py` recebe a requisição estruturada do Dialogflow e extrai o texto digitado pelo usuário.
4. **Camada de Inteligência e Recuperação (RAG & Ollama):**
   - O sistema gera o embedding da pergunta do usuário.
   - Realiza o cálculo de **Similaridade de Cosseno** comparando o vetor da pergunta com os vetores armazenados em `embedding.npy`.
   - Recupera os trechos mais relevantes da `base_conhecimento.txt`.
5. **Geração da Resposta Semântica:** O contexto recuperado é injetado junto com a pergunta em um prompt estrito e enviado ao modelo **Llama 3 (via Ollama)**, que gera a resposta final sem alucinações e a envia de volta ao Dialogflow.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3, Flask
- **Processamento Vetorial:** NumPy (Matrizes, vetores e Similaridade de Cosseno)
- **Modelos de IA (Locais):** Ollama — Modelo `llama3` (utilizado tanto para geração de texto quanto para criação de embeddings)
- **Processamento de Linguagem Natural (NLP):** Dialogflow ES (Google Cloud)
- **Persistência:** Arquivos binários `.npy` para cache de vetores de alta performance

---

## 📂 Estrutura de Organização do Código

O projeto segue as boas práticas de separação de conceitos:

```text
├── base_conhecimento/
│   ├── __init__.py
│   └── carregar_base.py     # Componente que lê e fragmenta o arquivo de texto
├── gerar_embedding/
│   ├── __init__.py
│   └── gerador.py           # Isolamento da API de embeddings do Ollama
├── templates/
│   └── index.html           # Interface web local com temática Gamer UI
├── .gitignore               # Arquivo para impedir o upload do ambiente virtual e do .npy
├── app.py                   # Ponto de entrada do Flask, configuração de rotas e do Webhook v2
├── base_conhecimento.txt    # Base de dados textual contendo os manuais técnicos de consoles
└── requirements.txt         # Gerenciador de dependências do ecossistema Python
