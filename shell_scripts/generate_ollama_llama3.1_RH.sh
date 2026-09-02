curl -N http://$OLLAMA_SERVER2:3000/api/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $WEBUI_API_KEY" \
  -d '{
    "model": "llama3.1:latest",
    "messages": [
      {"role": "user", "content": "quantos dias de férias eu tenho direito?"}
    
    ],
    "files": [
      {"type": "collection", "id": "c208c189-dec4-4bac-9009-3ce5cf13d52e"]
  }'