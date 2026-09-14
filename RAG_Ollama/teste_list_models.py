import numpy as np
import requests
import os
import json

ollama_server = os.environ["OLLAMA_SERVER2"]
OLLAMA_HOST = f"http://{ollama_server}:11434"
response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=10)
# print(response.json())
print(json.dumps(response.json(), indent=4))