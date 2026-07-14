import os 
from dotenv import load_dotenv

# Core LangChain Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# RAG & Chain Imports (Fixed Typo Here)

from langchain_classic.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)


from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)

# Your local imports
from app.rag.vectorstore import get_or_create_collection


# Load Environment Variables
load_dotenv()

# Initialize LLM globally 
# Model name "gemini-2.5-flash" works perfectly
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_ollama import ChatOllama

ollama_llm = ChatOllama(
    model="qwen2.5:latest",
    temperature=0,
    base_url="http://localhost:11434"
)

# Session history storage
session_histories: dict[str, list] = {}

def get_chat_history(session_id: str) -> list:
    return session_histories.get(session_id, [])


def build_rag_chain(session_id: str ):
    vectorstore = get_or_create_collection(session_id )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # Using the global ollama_llm instance directly to avoid "not callable" error
    current_llm = ollama_llm 

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Given the chat history and the latest user question, "
         "rewrite it as a standalone question. "
         "Do NOT answer it, just rephrase if needed, otherwise return as is."
         ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    history_aware_retriever = create_history_aware_retriever(
        current_llm, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful assistant. "
         "Use the following retrieved context to answer the question. "
         "If you don't know the answer, say you don't know. "
         "Keep the answer concise.\n\n"
         "Context:\n{context}"
         ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(current_llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain


def ask_question(session_id: str, question: str):
    try:
        print(f"[INFO] Building RAG chain for session: {session_id}")
        rag_chain = build_rag_chain(session_id)
        chat_history = get_chat_history(session_id)

        print(f"[INFO] Invoking chain with question: {question}")
        result = rag_chain.invoke({
            "input": question,
            "chat_history": chat_history
        })

        print(f"[INFO] Result keys: {result.keys()}")
        answer = result.get("answer", "Sorry, I could not generate an answer.")

        if session_id not in session_histories:
            session_histories[session_id] = []

        # Appending message history accurately
        session_histories[session_id].extend([
            HumanMessage(content=question),
            AIMessage(content=answer)
        ])

        sources = list(set([
            doc.metadata.get("source", "Unknown")
            for doc in result.get("context", [])
        ]))

        return answer, sources

    except Exception as e:
        print(f"[ERROR] ask_question failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e

async def stream_ask_question(session_id: str, question: str):
    try:
        print(f"[INFO] Building RAG chain for streaming session: {session_id}")
        rag_chain = build_rag_chain(session_id)
        chat_history = get_chat_history(session_id)

        print(f"[INFO] Invoking async stream with question: {question}")
        
        full_answer = ""
        
        async for chunk in rag_chain.astream({
            "input": question,
            "chat_history": chat_history
        }):
            print(chunk)
            if "answer" in chunk:
                full_answer += chunk["answer"]
                yield chunk["answer"]
        
        if session_id not in session_histories:
            session_histories[session_id] = []

        # Appending message history accurately after streaming completes
        session_histories[session_id].extend([
            HumanMessage(content=question),
            AIMessage(content=full_answer)
        ])

    except Exception as e:
        print(f"[ERROR] stream_ask_question failed: {str(e)}")
        import traceback
        traceback.print_exc()
        yield f"Error: {str(e)}"