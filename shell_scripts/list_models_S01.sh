### test the script to list LLM models available on the server

curl http://200.144.192.67:11434/api/tags | jq ".models[] | .name"  ### gera os nomes
### curl http://200.144.192.67:11434/api/tags | jq '[.models[] | select (.details.family | test("bert": "i")) | {name, digest, modified_at, family: .details.family}]'
# curl http://200.144.192.67:11434/api/tags | jq '[.models[] | select (.details.family == "bert" or .details.family == "nomic-bert") | {name, digest, modified_at, family: .details.family}]'
# curl http://200.144.192.67:11434/api/tags 

#-d '{  
#  "model": "nemotron-3-nano",  
#  "prompt": "quem é você?",  
#  "stream": false
#}' 