from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from typing import List, Tuple
import os
from dotenv import load_dotenv
from chroma_utils import vector_store

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# Define the retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# Define the prompt template
template = """
You are a helpful AI assistant. Use the following context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}

Question: {question}

Helpful Answer:"""

QA_PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# Custom get_chat_history function to handle our chat history format
def get_chat_history(chat_history: List[Tuple[str, str]]) -> str:
    buffer = ""
    for human_message, ai_message in chat_history:
        buffer += f"Human: {human_message}\nAI: {ai_message}\n"
    return buffer

def get_rag_chain(model="gpt-4o-mini"):
    # Get the OpenAI API key from environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    # Initialize the ChatOpenAI model with the API key
    llm = ChatOpenAI(
        temperature=0,
        model_name=model,
        openai_api_key=openai_api_key
    )

    # Create the conversational retrieval chain with our custom get_chat_history function
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        get_chat_history=get_chat_history
    )

    return qa_chain