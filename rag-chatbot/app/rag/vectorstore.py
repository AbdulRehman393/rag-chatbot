import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

PERSIST_DIR = os.path.join("data", "chroma")
COLLECTION = "docs"


def get_vectorstore():
    embeddings = OpenAIEmbeddings()
    vs = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIR,
    )
    return vs