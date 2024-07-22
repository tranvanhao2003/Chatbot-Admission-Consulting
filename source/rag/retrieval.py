from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.vectorstores import FAISS
from source.rag.process_data import ProcessData
from source.rag.load_model import load_embedding_model
from configs.load_config import LoadConfig
import dotenv
import os


APP_CONFIG = LoadConfig()

dotenv.load_dotenv()
# Initialize Embeddings
embedding = load_embedding_model()
VECTOR_DB_PATH = APP_CONFIG.persist_vector_directory


def create_retrivers():
    # load data parsed
    data_chunked = ProcessData().load_data_chunked()

    # initialize the bm25 retriever
    bm25_retriever = BM25Retriever.from_documents(data_chunked)
    bm25_retriever.k = APP_CONFIG.top_k
    
    
    #initialize the chroma retriever
    if not os.path.exists(VECTOR_DB_PATH):
        faiss_vectorstore = FAISS.from_documents(data_chunked, embedding)
        faiss_vectorstore.save_local(VECTOR_DB_PATH)
    else:
        faiss_vectorstore = FAISS.load_local(VECTOR_DB_PATH, embedding, allow_dangerous_deserialization=True)
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": APP_CONFIG.top_k, 
                                                                    "similarity_score": APP_CONFIG.similarity_score})

    # fusion FAISS and BM25
    ensemble_retriever = EnsembleRetriever(retrievers=[faiss_retriever, bm25_retriever],
                                           weights=[0.5, 0.5])
    
    # rerank with cohere
    compressor = CohereRerank(cohere_api_key=os.getenv("COHERE_API_KEY"))
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, 
        base_retriever=ensemble_retriever
    )
    return compression_retriever

if __name__ == "__main__":
    compression_retriever = create_retrivers()
