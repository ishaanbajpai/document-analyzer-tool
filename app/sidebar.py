import streamlit as st
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # Sidebar: Model Selection
    model_options = ["gpt-4o", "gpt-4o-mini"]

    st.sidebar.header("Configure", divider="gray")
    st.sidebar.subheader("Model", divider=True)
    st.sidebar.selectbox("Select Model", options=model_options, key="model", index=1)

    # Sidebar: Upload Document
    st.sidebar.subheader("Upload Document", divider=True)
    uploaded_files = st.sidebar.file_uploader("Choose files", type=["pdf", "docx", "html", "txt"], accept_multiple_files=True)
    if uploaded_files:
        if st.sidebar.button("Upload Selected Files"):
            with st.sidebar.status("Uploading files...") as status:
                success_count = 0
                for i, file in enumerate(uploaded_files):
                    progress_text = f"Uploading file {i+1}/{len(uploaded_files)}: {file.name}"
                    st.sidebar.text(progress_text)
                    upload_response = upload_document(file)
                    if upload_response:
                        success_count += 1

                if success_count > 0:
                    st.sidebar.success(f"Successfully uploaded {success_count} out of {len(uploaded_files)} files.")
                    st.session_state.documents = list_documents()  # Refresh the list after upload
                    status.update(label=f"Uploaded {success_count}/{len(uploaded_files)} files", state="complete")
                else:
                    status.update(label="Upload failed", state="error")

    # Sidebar: List Documents
    st.sidebar.subheader("Uploaded Documents", divider=True)
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})")

        # Delete Document
        st.sidebar.subheader("Delete Documents", divider=True)
        selected_file_id = st.sidebar.selectbox("Select a document to delete", options=[doc['id'] for doc in documents], format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))
        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
                    st.session_state.documents = list_documents()  # Refresh the list after deletion
                else:
                    st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")