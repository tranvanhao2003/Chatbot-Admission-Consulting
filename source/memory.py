import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain.memory import VectorStoreRetrieverMemory
from source.load_model import load_embedding_model
from utils.load_config import LoadConfig

APP_CONFIG = LoadConfig()

embed_model = load_embedding_model()

def create_memory():
    embedding_size = APP_CONFIG.vector_embed_size # dimension of the embedding model
    index =faiss.IndexFlatL2(embedding_size)
    vector_store = FAISS(embed_model.embed_query, 
                        index,
                        InMemoryDocstore({}), {})

    # Create VectorStoreRetrieverMemory
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    memory = VectorStoreRetrieverMemory(retriever=retriever, memory_key="chat_history", input_key="question")

    return memory