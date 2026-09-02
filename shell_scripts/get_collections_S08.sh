curl -s http://$OLLAMA_SERVER2:3000/api/v1/knowledge/ \
  -H "Authorization: Bearer $WEBUI_API_KEY" \
  | jq -r '.[] '