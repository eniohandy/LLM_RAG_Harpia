# ============================================================
# SETUP
# ============================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Avalia outputs RAG de um CSV.")
    parser.add_argument("--models-file", type=str, required=True)
    parser.add_argument("--data-file", type=str, required=True)
    args = parser.parse_args()

from imports import *

# ============================================================
# CONFIGURAÇÃO
# ============================================================

ollama_server = os.environ["OLLAMA_SERVER2"]
OLLAMA_HOST = f"http://{ollama_server}:11434"
OLLAMA_EMBED_MODEL = "qwen3-embedding:0.6b"
### aqui tem que verificar qual embedding usar. Pode ser tb bert e nomic-bert ###

# ============================================================
# FUNÇÕES
# ============================================================

### função para escolher o modelo -- tem que mudar para testar com todos.
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


### função que quebra o texto em chunks
def load_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        chunks = [line.strip() for line in file if line.strip()]

    if not chunks:
        raise ValueError(f"O arquivo de chunks está vazio: {file_path}")

    return chunks

### função que cria embeddings
def get_embeddings(texts):
    if isinstance(texts, str):
        texts = [texts]
    response = requests.post(
        f"{OLLAMA_HOST}/api/embed",
        headers={"Content-Type": "application/json"},
        json={"model": OLLAMA_EMBED_MODEL, "input": texts},
    )
    return response.json()["embeddings"]

### função de teste de similiridade entre a referência e os embeddings
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

### função de comparação retornando os melhores embeddings. Dá para ajustar no top_n para quantos quisermos.
def retrieve(query, document_embeddings, top_n=5):
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

### função resposta. baseado no melhor chunk encontrado, dá a resposta.
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

#parser = argparse.ArgumentParser(description="Executa um RAG usando chunks de um arquivo TXT.")
#parser.add_argument("caminho_txt", help="Caminho do arquivo TXT com um chunk por linha")
# args = parser.parse_args()

# chat_model = choose_chat_model()
# print(f"Modelo selecionado: {chat_model}")

print (args)

# PARTE I — Modelos

with open(args.models_file, "r", encoding="utf-8") as f:
    modelos = [linha.strip() for linha in f if linha.strip()]

print(modelos)