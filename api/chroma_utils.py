from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

#Initialze text splitter and embedding functions
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# Get the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

#Initialize ChromaDB vector store
vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def load_and_split_documents(file_path: str) -> List[Document]:
    if(file_path.endswith(".pdf")):
        loader = PyPDFLoader(file_path)
    elif(file_path.endswith(".docx")):
        loader = Docx2txtLoader(file_path)
    elif(file_path.endswith(".html")):
        loader = UnstructuredHTMLLoader(file_path)
    elif(file_path.endswith(".txt")):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file format")

    documents = loader.load()
    return text_splitter.split_documents(documents)

def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_documents(file_path)

        #add metadata to each split
        for split in splits:
            split.metadata["file_id"] = file_id

        vector_store.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False

def delete_doc_from_chroma(file_id: int) -> bool:
    try:
        docs = vector_store.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")

        vector_store._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")

        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False
