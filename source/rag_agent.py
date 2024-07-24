from langchain.agents import create_openai_tools_agent, Tool, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from source.agent.agent_SQL import Agent
from source.rag.chain_main import RAG
from langchain import hub
from utils.prompting.prompt import PROMPT_PDF_AGENT, PROMPTING_CSV_AGENT
from langchain_community.chat_message_histories import ChatMessageHistory
from configs.load_config import LoadConfig

APP_CFG = LoadConfig()
education_agent_prompt = hub.pull("hwchase17/openai-functions-agent")
memory = ChatMessageHistory(session_id="test-session")

def create_tools():
    tools = [
        Tool(
            name="Pdf Agent",
            func=RAG().get_qachain().invoke,
            description=PROMPT_PDF_AGENT
        ),
        Tool(
            name="Query Agent",
            func=Agent().agent.invoke,
            description=PROMPTING_CSV_AGENT
        ),
    ]
    return tools

def init_agent():
    tools = create_tools()
    education_agent = create_openai_tools_agent(
        llm=APP_CFG.load_groq_model(),
        prompt=education_agent_prompt,
        tools=tools
    )

    education_agent_excutor = AgentExecutor(
        agent=education_agent,
        tools=tools,
        return_intermediate_steps=False,
        verbose=True
    )

    # agent_with_chat_history = RunnableWithMessageHistory(
    #     education_agent_excutor,
    #     # This is needed because in most real world scenarios, a session id is needed
    #     # It isn't really used here because we are using a simple in memory ChatMessageHistory
    #     lambda session_id: memory,
    #     input_messages_key="input",
    #     history_messages_key="chat_history",
    # )

    return education_agent_excutor
