
import os
from typing import Optional, Tuple
from threading import Lock
import gradio as gr
from source.chain import ChatBot
from dotenv import load_dotenv
from source.process_data import ProcessData
load_dotenv()
# bot = ChatBot()

ProcessData().load_data_chunked()