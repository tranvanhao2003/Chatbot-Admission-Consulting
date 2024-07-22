from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.utilities import SQLDatabase
from utils.prompting.prompt import EXAMPLE_QUERY_SQL
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from source.rag.load_model import load_groq_model
from configs.load_config import LoadConfig

APP_CFG = LoadConfig()

class Agent:
    def __init__(self):
        self.db = self.prepare_db()
        self.llm = load_groq_model()
        self.full_prompt = self.create_prompt_agent()
        self.agent = self.create_agent()

    def prepare_db(self):
        db = SQLDatabase.from_uri(f"sqlite:///{APP_CFG.persist_database_directory}")
        return db

    def create_prompt_agent(self) -> ChatPromptTemplate:
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            EXAMPLE_QUERY_SQL,
            FastEmbedEmbeddings(),
            FAISS,
            k=2,
            input_keys=["input"],
        )

        system_prefix = """You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the given tools. Only use the information returned by the tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
        Note: You are only allowed to use Vietnamese to answer

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return "I don't know" as the answer.

        Here are some examples of user inputs and their corresponding SQL queries:"""

        few_shot_prompt = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=PromptTemplate.from_template(
                """User input: {input}
                SQL query: {query}"""
            ),
            input_variables=["input", "dialect", "top_k"],
            prefix=system_prefix,
            suffix="",
        )

        full_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate(prompt=few_shot_prompt),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        return full_prompt

    def create_agent(self):
        agent = create_sql_agent(
            llm=load_groq_model(),
            db=self.db,
            prompt=self.full_prompt,
            verbose=True,
            agent_type="openai-tools",
        )

        return agent

