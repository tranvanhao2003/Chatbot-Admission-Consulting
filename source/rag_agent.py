from langchain.agents import create_openai_tools_agent, Tool, AgentExecutor
from source.rag.chain import ChatBot
from source.agent.agent_SQL import Agent
from langchain import hub
from source.rag.load_model import load_groq_model


education_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

tools = [
    Tool(
        name="Parameter agent",
        func=Agent().agent.invoke,
        description="""Useful when you need to answer a question
        about questions with numbers such as salary, tuition, year of study, scores... of majors. Not useful for answering other questions, not related to information in the database. Use
        the entire prompt as input to the tool. For example, if the reminder is
        "How long does it take to study IT?", the input information must be
        "How long does it take to study IT?"".

        Note: You are only allowed to use Vietnamese to answer
        """,
    ),
    Tool(
        name="",
        func=ChatBot().chatbot.invoke,
        description="""Helpful in answering questions about introductions, job opportunities, support policies, and industry scholarships. Not useful when answering objective questions related to numbers such as years of study, salary, tuition... Use
        the entire prompt as input to the tool. Use the entire prompt as
        input to the tool. For example, if the reminder is
        “How long does it take to learn IT?”, the input information must be
        "How long does it take to learn IT?".
        
        Note: You are only allowed to use Vietnamese to answer
        """,
    ),
]

education_agent = create_openai_tools_agent(
    llm=load_groq_model(),
    prompt=education_agent_prompt,
    tools=tools
)

education_agent_excutor = AgentExecutor(
    agent=education_agent,
    tools=tools,
    return_intermediate_steps=False,
    verbose=True
)
