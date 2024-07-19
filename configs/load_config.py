import os
from dotenv import load_dotenv
import yaml
import shutil


load_dotenv()

class LoadConfig:
    def __init__(self) -> None:
        with open("./configs/config.yml") as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)
        
        self.load_directories(app_config=app_config)
        self.load_llm_config(app_config=app_config)
        self.load_chunk_config(app_config=app_config)
        self.load_retriver_config(app_config=app_config)

    def load_directories(self, app_config):
        # Load parameters directories from load_config.yml file 
        self.persist_vector_directory = (
            app_config['directories']['persist_vector_directory']
        )
        self.data_pdf_education_directory = (
            app_config['directories']['data_pdf_education_directory']
        )
        self.data_csv_education_directory = (
            app_config['directories']['data_csv_education_directory']
        )
        self.persist_chunk_directory = (
            app_config['directories']['persist_chunk_directory']
        )
    def load_llm_config(self, app_config):
        # Load parameters llm from load_config.yml file 
        self.rag_model = app_config['llm_config']['rag_model']
        self.temperature = app_config['llm_config']['temperature']
        self.max_token = app_config['llm_config']['max_token']
        self.summarize_model = app_config['llm_config']['summarize_model']
        
    def load_retriver_config(self, app_config):
        self.vector_embed_size = app_config['retriever_config']['vector_embed_size']
        self.similarity_score = app_config['retriever_config']['similarity_score']
        self.embedding_model = app_config['retriever_config']['embedding_model']
        self.top_k = app_config['retriever_config']['top_k']

    def load_chunk_config(self, app_config):
        self.model_chunk = app_config['chunk_config']['model_name']
        self.chunk_size = app_config['chunk_config']['chunk_size']
        self.chunk_overlap = app_config['chunk_config']['chunk_overlap']
        self.max_attempts = app_config['chunk_config']['max_attempts']
        self.delimiter = app_config['chunk_config']['delimiter']

    def remove_directory(self, directory_path: str): 
        """
        Removes the specified directory.

        Parameters:
            directory_path (str): The path of the directory to be removed.

        Raises:
            OSError: If an error occurs during the directory removal process.

        Returns:
            None
        """

        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
                print(
                    f"The directory '{directory_path}' has been successfully removed.")
            except OSError as e:
                print(f"Error: {e})")
        else:
            print(f"The directory '{directory_path}' does not exist.")  
