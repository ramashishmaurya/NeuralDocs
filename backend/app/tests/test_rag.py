from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen2.5:latest")

result  = llm.invoke("waht is full form of ai ")

print(result.content)