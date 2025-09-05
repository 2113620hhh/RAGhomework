import os
from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from .corpus_loader import load_corpus


def get_vector_store(corpus_path, persist_directory="./chroma_db"):
    """获取或创建向量存储"""
    embeddings = HuggingFaceEmbeddings(
        #model_name=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        model_name=os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    )

    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print("加载现有向量数据库")
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
    else:
        print("创建新向量数据库")
        documents = load_corpus(corpus_path)
        print(f"处理了 {len(documents)} 个文档块")
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        #vector_store.persist()
        print("向量数据库创建完成并已持久化")
        return vector_store