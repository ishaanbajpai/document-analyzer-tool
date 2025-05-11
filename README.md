# Document Analyzer Support Tool

A powerful tool that allows you to upload documents, analyze them using AI, and ask questions about their content. This application uses LangChain, OpenAI, and vector databases to provide intelligent responses based on your document content.

## Features

### Document Management
- **Multi-select File Upload**: Upload multiple documents at once (PDF, DOCX, HTML, TXT)
- **Document Listing**: View all uploaded documents with timestamps
- **Document Deletion**: Remove documents when no longer needed

### AI-Powered Analysis
- **Question Answering**: Ask questions about your documents and get accurate answers
- **Context-Aware Responses**: The AI understands the context of your questions and provides relevant information
- **Chat History**: Maintain conversation history for more coherent interactions
- **Multiple AI Models**: Choose between different OpenAI models (GPT-4o, GPT-4o-mini)

### User Interface
- **Streamlit Web Interface**: Clean, intuitive interface for interacting with the system
- **FastAPI Backend**: Robust API for handling document processing and AI interactions
- **Real-time Updates**: See document uploads and AI responses in real-time

## Setup Instructions

### Prerequisites
- Python 3.9+ installed
- OpenAI API key
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ishaanbajpai/document-analyzer-tool.git
   cd document-analyzer-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Create a `.env` file in the root directory based on `.env.sample`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. **Create necessary directories**
   ```bash
   mkdir -p temp chroma_db
   ```

### Running the Application

1. **Start the FastAPI backend**
   ```bash
   cd api
   python -m uvicorn main:app --reload
   ```

2. **Start the Streamlit frontend** (in a new terminal)
   ```bash
   cd app
   streamlit run streamlit_app.py
   ```

3. **Access the application**
   - Open your browser and go to: http://localhost:8501

## Usage Guide

1. **Uploading Documents**
   - Use the sidebar to upload one or more documents
   - Click "Upload Selected Files" to process the documents
   - Wait for confirmation that the documents have been processed

2. **Asking Questions**
   - Type your question in the chat input box
   - Select the AI model you want to use
   - Press Enter or click the send button
   - The AI will analyze your documents and provide an answer

3. **Managing Documents**
   - View the list of uploaded documents in the sidebar
   - Click the delete button next to a document to remove it

## Troubleshooting

- **API Connection Issues**: Ensure the FastAPI server is running on port 8000
- **Document Upload Failures**: Check that the temp directory exists and has write permissions
- **AI Response Errors**: Verify your OpenAI API key is correct and has sufficient credits

## Technical Architecture

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI (Python)
- **Vector Database**: ChromaDB
- **Document Processing**: LangChain document loaders and text splitters
- **Embedding Model**: OpenAI Embeddings
- **LLM Integration**: LangChain with OpenAI models

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with LangChain, OpenAI, FastAPI, and Streamlit
- Vector search powered by ChromaDB
