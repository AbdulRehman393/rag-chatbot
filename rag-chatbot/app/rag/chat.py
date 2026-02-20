import os
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from .vectorstore import get_vectorstore

def format_docs(docs) -> str:
    return "\n\n".join([d.page_content for d in docs])

def build_chain():
    llm = ChatOpenAI(
        model=os.getenv("OPENROUTER_MODEL"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0,
    )

    vs = get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template(
        """Use the provided context to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}"""
    )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

def answer(question: str):
    return build_chain().invoke(question)