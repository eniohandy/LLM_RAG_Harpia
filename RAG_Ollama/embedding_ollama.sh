curl http://$OLLAMA_SERVER2:11434/api/embed \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "input": ["teste de embedding de RH"]
  }'
