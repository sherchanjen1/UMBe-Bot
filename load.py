import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def ingest_documents(file_path, persist_directory):
    try:
        print(f"🔍 Loading: {file_path}")
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        if not docs:
            print(f"⚠️ No content found in: {file_path}")
            return

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = splitter.split_documents(docs)

        if not split_docs:
            print(f"⚠️ Document splitting failed for: {file_path}")
            return

        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=OpenAIEmbeddings(),
            persist_directory=persist_directory
        )
        vectorstore.persist()
        print(f"✅ Indexed: {file_path} → [{persist_directory}]")

    except Exception as e:
        print(f"❌ Failed to process {file_path}: {e}")

if __name__ == "__main__":
    base_path = "course_materials"

    if not os.path.exists(base_path):
        print(f"❌ Error: Folder '{base_path}' does not exist.")
        exit()

    for instructor in os.listdir(base_path):
        folder_path = os.path.join(base_path, instructor)
        if os.path.isdir(folder_path):
            index_name = instructor.lower().replace(" ", "_").replace(".", "").replace("-", "_")
            persist_directory = f"course_index_ai4all_{index_name}"

            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith(".pdf"):
                    file_path = os.path.join(folder_path, file_name)
                    ingest_documents(file_path, persist_directory)
