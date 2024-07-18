from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
import dotenv
from source.retrieval import create_retrivers
from source.load_model import load_groq_model, load_embedding_model
from source.prompt import _TEMPLATE_EDUCATION, TEMPLATE_EDUCATION
from source.memory import create_memory

dotenv.load_dotenv()

class ChatBot:
    def __init__(self):
        self.compression_retriever = create_retrivers()
        self.embed_model = load_embedding_model()
        self.LLM = load_groq_model()
        self.memory = create_memory()


    # Instantiate the Retrieval Question Answering Chain
    def get_condense_prompt_qa_chain(self):

        CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_TEMPLATE_EDUCATION)
       
        QA_PROMPT = PromptTemplate(template=TEMPLATE_EDUCATION, 
                                   input_variables=["question", "context"])

        model = ConversationalRetrievalChain.from_llm(
            llm=self.LLM,
            retriever=self.compression_retriever,
            memory=self.memory,
            condense_question_prompt=CONDENSE_QUESTION_PROMPT,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT})
        
        return model

if __name__ == "__main__":
    bot = ChatBot()

    chain = bot.get_condense_prompt_qa_chain()
    response = chain.invoke({"question": "tôi muốn xem giới thiệu ngành công nghệ thông tin"})
    print(response['answer'])
