# Mini RAG Document Q&A

This project is a simple **Retrieval-Augmented Generation (RAG)** application that allows users to upload documents and ask questions based only on the content of those documents.

The application is built using **Streamlit**, **LangChain**, **Chroma**, **HuggingFace embeddings**, and **Groq LLM**.

---

## 🚀 Features

- Upload multiple **PDF or TXT documents**
- Convert documents into **vector embeddings**
- Store embeddings in **Chroma vector database**
- Ask questions through a **chat-style UI**
- Answers are generated **only from uploaded documents**
- Returns **"I don’t know based on the given documents."** if the answer is not found
- Prevents hallucination

---

## 🧠 Tech Stack

- **Python**
- **Streamlit** – Web UI
- **LangChain** – RAG pipeline
- **Chroma** – Vector database
- **HuggingFace (sentence-transformers)** – Text embeddings
- **Groq (LLaMA 3.1)** – Large Language Model

---

## 📂 Project Structure

```

Mini-RAG-Document-QA/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/

````

---

## ⚙️ How It Works

1. User uploads documents (PDF/TXT)
2. Documents are split into chunks
3. Chunks are converted into vectors using HuggingFace embeddings
4. Vectors are stored in Chroma
5. User question is converted into a vector
6. Relevant document chunks are retrieved using similarity search
7. Groq LLM generates an answer using retrieved context only
---

## 📌 Notes

* `venv/`, `.env`, and `chroma_db/` are ignored using `.gitignore`
* This project is designed as a **take-home assignment / mini RAG demo**

---

## ✅ Outcome

A working end-to-end **Document Question Answering system** using RAG principles.

---