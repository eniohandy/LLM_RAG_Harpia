# Algumas info sobre este repositório


    .<br>
    ├── RAG/                        # Esta pasta contém scripts para testes com modelos pagos (claude e gemini, via openrouter)<br>
    ├── RAG_Ollama/                 # Esta pasta contém scripts para testes com Ollama e modelos abertos.<br>
    ├── shell_script/               # Esta pasta contém scripts para testes básicos e de conectividade com Ollama, WebUI e modelos no servidor.<br>
    ├── shell_script_external/      # Esta pasta contém testes de conectividade com provedores externos, OpenAI e Openrouter<br>
    ├── README.md                   # Este arquivo<br>
    └── to do                       # ainda não desenvolvido<br>

A well-organized repository structure enhances readability and maintainability. Below is a recommended file structure:

    .
    ├── data/                 # Contains links to datasets. If the repository is or will be public, you can upload the datasets directly here
    ├── images/               # Contains images (avoid uploading too many images to private repositories)
    ├── scripts/              # Python or other language scripts (e.g., shell scripts for running experiments)
    ├── src/                  # Project source code
    ├── utils/                # Contains common code that is reusable and independent of the application's core logic
    ├── .gitignore            # File extensions or patterns to be ignored by Git
    ├── LICENSE               # Repository license
    ├── main.py               # Python script that contains an easy-to-run code example of the project
    ├── README.md             # Project overview. Should include a simple tutorial of how to use the main.py file
    └── requirements.txt      # Dependencies (preferably use pip instead of conda environments)


## Orientação geral

Este repositório foi desenvolvido com o propósito de testar funcionalidades de RAG.
Estas funcionalidades podem ser verificadas em modelos LLM particulares (como Claude e Gemini).
A solução implementada usa o Openrouter.

