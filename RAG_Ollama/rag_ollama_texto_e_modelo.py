import numpy as np
import requests
import os
import argparse

# ============================================================
# CONFIGURAÇÃO
# ============================================================

ollama_server = os.environ["OLLAMA_SERVER2"]
OLLAMA_HOST = f"http://{ollama_server}:11434"
OLLAMA_EMBED_MODEL = "qwen3-embedding:0.6b"


# ============================================================
# FUNÇÕES
# ============================================================

def choose_chat_model():
    response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=10)
    response.raise_for_status()

    models = [model["name"] for model in response.json().get("models", [])]
    if not models:
        raise RuntimeError("Nenhum modelo foi encontrado no servidor Ollama.")

    print("\nModelos LLM disponíveis:")
    for index, model in enumerate(models, start=1):
        print(f"  {index}. {model}")

    while True:
        choice = input("Escolha o número do modelo LLM: ").strip()
        try:
            model_index = int(choice) - 1
        except ValueError:
            print("Digite um número válido.")
            continue

        if 0 <= model_index < len(models):
            return models[model_index]

        print(f"Escolha um número entre 1 e {len(models)}.")


def load_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        chunks = [line.strip() for line in file if line.strip()]

    if not chunks:
        raise ValueError(f"O arquivo de chunks está vazio: {file_path}")

    return chunks


def get_embeddings(texts):
    if isinstance(texts, str):
        texts = [texts]
    response = requests.post(
        f"{OLLAMA_HOST}/api/embed",
        headers={"Content-Type": "application/json"},
        json={"model": OLLAMA_EMBED_MODEL, "input": texts},
    )
    return response.json()["embeddings"]


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query, document_embeddings, top_n=2):
    response = requests.post(
        f"{OLLAMA_HOST}/api/embed",
        headers={"Content-Type": "application/json"},
        json={"model": OLLAMA_EMBED_MODEL, "input": query},
    )
    query_embedding = np.array(response.json()["embeddings"][0])

    scored = []
    for doc in document_embeddings:
        score = cosine_similarity(query_embedding, np.array(doc["embedding"]))
        scored.append({"text": doc["text"], "score": float(score)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


def generate_answer(query, context_docs):
    context = "\n\n".join(
        f"[{i+1}] {doc['text']}" for i, doc in enumerate(context_docs)
    )

    response = requests.post(
        f"{OLLAMA_HOST}/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": chat_model,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": "Responda a pergunta do usuário com base apenas no contexto fornecido. Cite o número da fonte entre colchetes.",
                },
                {
                    "role": "user",
                    "content": f"Contexto:\n{context}\n\nPergunta: {query}",
                },
            ],
        },
    )

    return response.json()["choices"][0]["message"]["content"]


# ============================================================
# EXECUÇÃO
# ============================================================

parser = argparse.ArgumentParser(description="Executa um RAG usando chunks de um arquivo TXT.")
parser.add_argument("caminho_txt", help="Caminho do arquivo TXT com um chunk por linha")
args = parser.parse_args()

chat_model = choose_chat_model()
print(f"Modelo selecionado: {chat_model}")

# PARTE I — Chunks de texto
chunks = load_chunks(args.caminho_txt)

# PARTE II/III — Indexar os chunks (gerar e guardar os embeddings)
embeddings = get_embeddings(chunks)
document_embeddings = [
    {"text": chunks[i], "embedding": embeddings[i]}
    for i in range(len(chunks))
]

print(f"Indexados {len(document_embeddings)} chunks, cada um com {len(document_embeddings[0]['embedding'])} dimensões")

# PARTE IV — Buscar os chunks mais relevantes pra pergunta
query = "quem tem direito à vale alimentação e refeição?"
results = retrieve(query, document_embeddings, top_n=2)

print("\nDocumentos recuperados:")
for i, r in enumerate(results):
    print(f"  {i+1}. (score: {r['score']:.4f}) {r['text']}")

# PARTE V — Gerar a resposta final
answer = generate_answer(query, results)
print(f"\nPergunta: {query}")
print(f"Resposta: {answer}")
