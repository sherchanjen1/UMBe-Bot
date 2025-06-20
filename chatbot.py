from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os

load_dotenv()

def ask_umassbot(query, course=None, module=None):
    # Normalize vague queries
    vague_queries = ["tell me everything", "give me everything"]
    if query.lower().strip() in vague_queries:
        query = "Summarize all key assignments, reflections, and materials from this instructor's module."

    # Default directory
    persist_directory = "course_index"

    if course == "AI for All" and module:
        index_name = module.lower().replace(" ", "_").replace(".", "").replace("-", "_")
        persist_directory = f"course_index_ai4all_{index_name}"

    # Check if vector store exists
    if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
        return f"⚠️ Sorry, I couldn't find documents for: {module}"

    # Load vectorstore and QA chain
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        retriever=retriever,
        return_source_documents=False
    )

    result = chain.invoke(query)
    return result["result"]
