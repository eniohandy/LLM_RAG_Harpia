curl -N http://$OLLAMA_SERVER2:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
  "model": "cogito",
  "think": false,
  "messages": [
    {"role": "system", "content": "As informações RAG são separadas por <|RAG|> no começo e no fim. A pergunta é separada por <|Pergunta|> no começo e no fim."},
    {"role": "user", "content": "que dia é hoje?"} 
  ],
  "temperature": 0.0,
  "seed": 17
}' 