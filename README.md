
# Dependency Installation:
`pip install steamlit langchain openai wikipedia chromadb tiktoken`
steamlit - used to build the app
langchain - used to build llm workflow
openai - needed to use openai gpt
wikipedia - used to connect gpt to wikipedia
chromadb - vector storage...next tut?
tiktoken - backend tokenizer for openai

# OpenAI key setup
1. Retrieve an OpenAI API key from https://platform.openai.com/account/api-keys
2. Set your secret key to a variable called `api_key` in a file called `apikey.py` at the root of this repository.

# Usage
`streamlit run app.py`

# Credit
Produced with the guidance of [Nicholas Renotte](https://github.com/nicknochnack)'s [LangChain Crash Course: Build a AutoGPT app in 25 minutes!](https://www.youtube.com/watch?v=MlK6SIjcjE8)