from langchain.memory import (
    ConversationBufferWindowMemory, 
    ConversationEntityMemory,
    CombinedMemory
)
from configs.load_config import LoadConfig

APP_CONFIG = LoadConfig()

def create_memory():
    memory_windown = ConversationBufferWindowMemory(
        k=2,
        memory_key="chat_history",
        return_messages=True,
        input_key="question")

    return memory_windown
