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
- Python 3.9+ installed (Python 3.9 or 3.10 recommended for best compatibility)
- OpenAI API key
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ishaanbajpai/document-analyzer-tool.git
   cd document-analyzer-tool
   ```

2. **Install dependencies**

   Option 1: Using requirements.txt (recommended)
   ```bash
   pip install -r requirements.txt
   ```

   Option 2: If you encounter issues with the requirements.txt file, install the dependencies manually in this exact order:
   ```bash
   # Core dependencies
   pip install pydantic==1.10.8
   pip install python-dotenv==1.0.0
   pip install requests==2.31.0

   # FastAPI and Streamlit
   pip install fastapi==0.95.2 uvicorn==0.22.0 python-multipart==0.0.6
   pip install streamlit==1.24.0

   # LangChain - note the underscore vs hyphen difference!
   pip install langchain-core==0.1.23
   pip install langchain==0.0.267
   pip install langchain_community==0.0.10
   pip install langchain_openai==0.0.2

   # Vector database and document processing
   pip install chromadb==0.4.18
   pip install pypdf==3.15.1 python-docx==0.8.11 docx2txt==0.8

   # OpenAI and utilities
   pip install openai==0.28.1
   pip install tqdm==4.66.1 numpy==1.24.3 pandas==2.0.3
   ```

   **Important Note**: Pay special attention to the package names. Some packages use hyphens (`langchain-core`) while others use underscores (`langchain_community`). This is a common source of installation issues.

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

### Connection Issues
- **API Connection Issues**: Ensure the FastAPI server is running on port 8000
- **Document Upload Failures**: Check that the temp directory exists and has write permissions
- **AI Response Errors**: Verify your OpenAI API key is correct and has sufficient credits

### Dependency Issues
- **LangChain Installation Problems**: If you encounter errors with LangChain dependencies, try the manual installation method provided in the Installation section
- **Version Conflicts**: Create a fresh virtual environment to avoid conflicts with existing packages
- **ImportError or ModuleNotFoundError**: Ensure you're using a compatible Python version (3.9 or 3.10 recommended)

### Common Errors and Solutions
- **"No module named 'langchain'"**: Try installing langchain manually with `pip install langchain==0.0.267`
- **"No module named 'langchain_community'"**: Install with `pip install langchain_community==0.0.10` (note the underscore, not hyphen)
- **"No module named 'langchain_openai'"**: Install with `pip install langchain_openai==0.0.2` (note the underscore, not hyphen)
- **"No module named 'chromadb'"**: Install with `pip install chromadb==0.4.18`
- **OpenAI API errors**: Make sure you're using `openai==0.28.1` which is compatible with the older LangChain version
- **Import errors after installing dependencies**: Try restarting your Python environment or terminal
- **Package naming confusion**: Some LangChain packages use hyphens in PyPI (when installing with pip) but underscores in Python imports

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
