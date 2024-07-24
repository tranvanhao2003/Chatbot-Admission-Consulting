from langchain.prompts import PromptTemplate
from utils.prompting.prompt import TEMPLATE_EDUCATION
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from configs.load_config import LoadConfig
import dotenv
import os


APP_CONFIG = LoadConfig()
dotenv.load_dotenv()

# Initialize Embeddings
VECTOR_DB_PATH = APP_CONFIG.persist_vector_directory


class RAG:
    def __init__(self):
        self.prompt = PromptTemplate(template=TEMPLATE_EDUCATION, 
                                    input_variables=["question", "context"])
        self.data_chunked = self.load_data()
        self.embedding_model = APP_CONFIG.load_embedding_model()
        self.retriever = self.init_retriever()
        self.llm = APP_CONFIG.load_groq_model()

    def load_data(self) -> RecursiveCharacterTextSplitter:
        """
        Load file PDF using PyMuPDFLoader
        """
        DATA_PATH = APP_CONFIG.data_pdf_education_directory
        loader = PyMuPDFLoader(DATA_PATH)
        documents = loader.load()

        docs = RecursiveCharacterTextSplitter(
            chunk_size=APP_CONFIG.chunk_size,
            chunk_overlap=APP_CONFIG.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        ).split_documents(documents=documents)
        return docs


    def init_retriever(self):
        # initialize the bm25 retriever
        bm25_retriever = BM25Retriever.from_documents(self.data_chunked)
        bm25_retriever.k = APP_CONFIG.top_k
        
        
        #initialize the chroma retriever
        if not os.path.exists(VECTOR_DB_PATH):
            faiss_vectorstore = FAISS.from_documents(self.data_chunked, self.embedding_model)
            faiss_vectorstore.save_local(VECTOR_DB_PATH)
        else:
            faiss_vectorstore = FAISS.load_local(VECTOR_DB_PATH, self.embedding_model, allow_dangerous_deserialization=True)
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


    def format_docs(self, docs: list):
        return "\n\n".join(doc.page_content for doc in docs)
    def get_qachain(self):
        rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain

# if __name__ == "__main__":
# rag = RAG()
# print(rag.get_qachain().invoke("cơ hội việc làm của ngành CNTT"))