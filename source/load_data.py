from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.load_config import LoadConfig

APP_CONFIG = LoadConfig()
DATA_PATH = APP_CONFIG.data_csv_education_directory


def load_data():
    DATA_PATH = APP_CONFIG.data_csv_education_directory
    loader = CSVLoader(DATA_PATH, csv_args={
                        "delimiter": ","})
    documents = loader.load()
    # Split loaded documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=APP_CONFIG.chunk_size, 
                                                   chunk_overlap=APP_CONFIG.chunk_overlap)
    
    documents = text_splitter.split_documents(documents=documents)

    return documents
