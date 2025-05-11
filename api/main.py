from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from langchain_utils import get_rag_chain
from db_utils import insert_application_logs, get_chat_history, get_all_documents, insert_document_record, delete_document_record
from chroma_utils import index_document_to_chroma, delete_doc_from_chroma
import os
import uuid
import logging
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

# API endpoints begins

#chat endpoint
@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id or str(uuid.uuid4())
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}")

    chat_history = get_chat_history(session_id)

    # Get the model value
    model_value = query_input.model  # Now model is a simple string

    # Convert chat history to the format expected by the older LangChain API
    formatted_history = []
    for i in range(0, len(chat_history), 2):
        if i+1 < len(chat_history):
            # Extract the content from the dictionaries and create a tuple of strings
            human_message = chat_history[i]["content"]
            ai_message = chat_history[i+1]["content"]
            formatted_history.append((human_message, ai_message))

    rag_chain = get_rag_chain(model_value)
    result = rag_chain({"question": query_input.question, "chat_history": formatted_history})
    answer = result["answer"]

    insert_application_logs(session_id, query_input.question, answer, model_value)
    logging.info(f"Session ID: {session_id}, AI Response: {answer}")
    return QueryResponse(answer = answer, session_id = session_id, model = query_input.model)

@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = ['.pdf', '.docx', '.txt', '.html']
    file_extensions = os.path.splitext(file.filename)[1].lower()

    logging.info(f"File extension: {file_extensions}")

    if file_extensions not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, TXT, and HTML files are allowed.")

    temp_file_path = f"temp/{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = insert_document_record(file.filename)
        success = index_document_to_chroma(temp_file_path, file_id)

        if success:
                return {"message": f"File {file.filename} has been successfully uploaded and indexed.", "file_id": file_id}
        else:
                delete_document_record(file_id)
                raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()


@app.post("/delete-doc")
def delete_doc(request : DeleteFileRequest):
    chroma_delete_success = delete_doc_from_chroma(request.file_id)
    if chroma_delete_success:
        db_delete_success = delete_document_record(request.file_id)
        if db_delete_success:
            return {"message": f"Successfully deleted document with file_id {request.file_id} from the system."}
        else:
            return {"error": f"Deleted from Chroma but failed to delete document with file_id {request.file_id} from the database."}
    else:
        return {"error": f"Failed to delete document with file_id {request.file_id} from Chroma."}

