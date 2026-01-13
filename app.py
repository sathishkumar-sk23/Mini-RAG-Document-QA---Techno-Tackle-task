import streamlit as st
import os
from dotenv import load_dotenv


from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Mini RAG Document Q&A", layout="wide")
st.title("Mini RAG - Document Q&A (Chroma + Groq)")

# Session state
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

# Sidebar
st.sidebar.header("Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_documents(files):
    documents = []
    for file in files:
        file_path = os.path.join(DATA_DIR, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        if file.name.endswith(".pdf"):

            
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)

        documents.extend(loader.load())
    return documents

# Process documents
if uploaded_files and st.sidebar.button("Process Documents"):
    with st.spinner("Processing documents..."):
        docs = load_documents(uploaded_files)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=80
        )
        chunks = splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vector_db = Chroma.from_documents(
            chunks,
            embedding=embeddings,
            persist_directory="chroma_db"
        )

        vector_db.persist()
        st.session_state.vector_db = vector_db

        st.success("Documents processed and stored in Chroma!")

# Chat
st.header("Ask a Question")
query = st.text_input("Enter your question")

if query:
    if st.session_state.vector_db is None:
        st.warning("Please upload and process documents first.")
    else:
        docs = st.session_state.vector_db.similarity_search(query, k=3)

        if not docs:
            st.write("I don’t know based on the given documents.")
        else:
            context = "\n".join([doc.page_content for doc in docs])

            prompt = f"""
You are a document-based assistant.
Answer ONLY from the context below.
If the answer is not present, say:
"I don’t know based on the given documents."

Context:
{context}

Question:
{query}
"""

            llm = ChatGroq(
                model_name="llama-3.1-8b-instant",
                temperature=0
            )

            response = llm.invoke(prompt)
            st.write(response.content)
