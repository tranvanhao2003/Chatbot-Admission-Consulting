from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document
from configs.load_config import LoadConfig
from utils.summarize_chunk.chunker import auto_chunk
from utils.summarize_chunk.summary import get_chunk_summary
import os
import pickle

APP_CONFIG = LoadConfig()

class ProcessData:
    def __init__(self):
        self.documents = self.load_data_from_csv()
        self.auto_chunk_list = self.chunking_data()

    def load_data_from_csv(self):
        """
        Load file CSV using CSVLoader
        """
        DATA_PATH = APP_CONFIG.data_csv_education_directory
        loader = CSVLoader(DATA_PATH, csv_args={
                            "delimiter": ","})
        documents = loader.load()

        return documents

    def chunking_data(self) -> list:

        """
        Chunking document into paragraphs
        """
        docs_sum = ""
        for doc in self.documents:
            docs_sum += doc.page_content

        auto_chunk_list=auto_chunk(document=docs_sum, 
                                max_chunk_size=APP_CONFIG.chunk_size,
                                model_name=APP_CONFIG.model_chunk)    
        return auto_chunk_list

    def save_data_chunked(self)-> None:
        """
        Save data chunked into pikle file
        """
        data_chunked = []

        for chunk in self.auto_chunk_list:
            tuple_chunk_summarize = ({"content: ": chunk},  {"summarize: ": get_chunk_summary(chunk)})
            data_chunked.append(Document(
                page_content= '\n'.join(map(str, tuple_chunk_summarize))))
        with open(APP_CONFIG.persist_chunk_directory, mode='wb') as file:
            pickle.dump(data_chunked, file)
            
            # file.write(get_global_summary(chunks))

    def load_data_chunked(self) -> list:
        """Load data chunked"""
        persist_data_chunked = APP_CONFIG.persist_chunk_directory
        if not os.path.exists(persist_data_chunked):
            self.save_data_chunked()
        else:
            with open(persist_data_chunked, 'rb') as file:
                data_chunked = pickle.load(file)
        
            return data_chunked



