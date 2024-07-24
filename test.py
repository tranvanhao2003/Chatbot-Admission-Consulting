
# from source.rag.chain_main import RAG
# from source.rag_agent import init_agent
from source.agent.agent_SQL import Agent

agent = Agent()

print(agent.db.run("SELECT diem FROM TVTS WHERE Nganh = 'CÔNG NGHỆ THÔNG TIN'"))


# rag = RAG()
# chain = rag.get_qachain()
# print(chain.invoke({"question": "cơ hội việc làm cho ngành Kỹ thuật Robot và Trí tuệ nhân tạo"}))
# import time

# t1 = time.time()
# agent = init_agent()
# # response1 = agent.invoke({"input": "Hello"},
# #                         config={"configurable": {"session_id": "<foo>"}})
# response1 = agent.invoke({"input": "Ngành CNTT lấy bao nhiêu điểm"})['output']
#                         # config={"configurable": {"session_id": "<foo>"}})

# t2 = time.time() - t1
# print("="* 50 )
# print(response1)
# print(t2)