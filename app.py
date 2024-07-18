import streamlit as st
from source.chain import ChatBot
from utils.fewsort_spelling import spelling_correct_sentences
bot = ChatBot()


chain = bot.get_condense_prompt_qa_chain()

def respond(query: str) -> str:
    response = chain.invoke({"question": query})
    return response['answer']

# deploy model using streamlit
st.set_page_config(page_title="Chatbot TVTS", page_icon=":robot_face:")


with st.sidebar:
    st.header("About")
    st.markdown(
        """
        Đây là 1 giao diện chatbot
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        được thiết kế để hỏi đáp, tư vấn tuyển sinh.
        """
    )

    st.header("Các câu hỏi mẫu bạn có thể hỏi")
    st.markdown("- Ngành công nghệ thông tin học trong bao lâu")
    st.markdown("- Tổ hợp xét tuyển ngành kỹ thuật ô tô")
    st.markdown(
        "- Mức học phí ngành kỹ thuật cơ điện tử."
    )
    st.markdown("- Cơ hội việc làm cho ngành du lịch địa chất.")
    st.markdown(
        "- Mức lương của sinh viên CNTT CLC sau khi ra trường là?"
    )
    st.markdown("- Giới thiệu ngành kỹ thuật Robot và Trí tuệ nhân tạo")
    st.markdown("- Thời gian và học phí ngành khoa học dữ liệu")
    st.markdown("- Các chính sách dành hco ngành kỹ thuật ô tô")
    st.markdown("- Mã ngành của kỹ thuật cơ khí động lực là?")


st.markdown("""
<div style="text-align: center;">
            <img src="https://blogs.perficient.com/files/lanchain.png" alt="Chatbot Logo" width="100"/>
    <img src="https://img.freepik.com/premium-vector/robot-icon-chat-bot-sign-support-service-concept-chatbot-character-flat-style_41737-796.jpg?" alt="Chatbot Logo" width="200"/>
    <h1 style="color: #0078D7;">Chatbot Tư Vấn Tuyển Sinh</h1>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<p style="text-align: center; font-size: 18px; color: #555;">
    Xin chào! Rất vui khi được hỗ trợ anh/chị trong việc tìm kiếm thông tin.
</p>
""", unsafe_allow_html=True)


st.markdown("<hr/>", unsafe_allow_html=True)

user_query = st.text_input("Enter your question:", placeholder="E.g., What is the aim of AI act?")

if st.button("Answer"):
    user_query = spelling_correct_sentences(user_query)
    bot_answer = respond(user_query)
   
    st.markdown(f"""
    <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-top: 20px;">
        <h4 style="color: #0078D7;">Bot's Response:</h4>
        <p style="color: #335;">{bot_answer}</p>
    </div>
    """, unsafe_allow_html=True)
