import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from .vectorstore import get_vectorstore

SUPPORTED = {".pdf", ".txt", ".md"}


def load_docs(filepath: str):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(filepath)
    elif ext in {".txt", ".md"}:
        loader = TextLoader(filepath, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported: {SUPPORTED}")
    return loader.load()


def chunk_docs(docs: List, chunk_size=800, chunk_overlap=120):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)


def ingest_file(filepath: str):
    docs = load_docs(filepath)
    chunks = chunk_docs(docs)
    vs = get_vectorstore()
    vs.add_documents(chunks)
    vs.persist()
    return len(chunks)