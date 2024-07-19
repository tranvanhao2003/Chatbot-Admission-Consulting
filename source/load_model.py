from haystack.components.embedders import HuggingFaceAPITextEmbedder
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from haystack.utils import Secret
import os
from langchain_groq import ChatGroq
from configs.load_config import LoadConfig


APP_CONFIG = LoadConfig()

def load_embedding_model():
    embedding_model = FastEmbedEmbeddings(model_name=APP_CONFIG.embedding_model)
    return embedding_model

def load_groq_model():
    """
    Load GROQ model using API
    """
    langchain_groq = ChatGroq(
            model=APP_CONFIG.rag_model,
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=APP_CONFIG.temperature,
            max_tokens=APP_CONFIG.max_token,
            verbose=True,
        )
    return langchain_groq