curl -N http://$OLLAMA_SERVER2:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
  "model": "gemma4",
  "messages": [
    {"role": "system", "content": "As informações RAG são separadas por <|RAG|> no começo e no fim. A pergunta é separada por <|Pergunta|> no começo e no fim."},
    {"role": "user", "content": " <|RAG|>A média é a soma aritimetica das provas. Serão realizadas 3 provas. Há um ponto adicional na entrega dos trabalhos. Há três trabalhos, cada um correspondendo a uma prova. A média necessária para passar é 5.<|RAG|> <|Pergunta|>tirei 5 nas duas primeiras provas e fiz o trabalho antes da terceira prova. Quanto preciso tirar na terceira prova para passar? <|Pergunta|>"}
  ],
  "temperature": 0.0,
  "seed": 17
}'