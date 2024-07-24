_TEMPLATE_EDUCATION = """
        Provide the history of the most recent conversation and a follow-up question, which usually contains information related to the history.
        Let's ask that question again based on the given history. If you don't know, say "I don't understand your question.", don't try to make up the answer.
        Then answer the question correctly.
        Note: you can only use Vietnamese to answer.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:"""

TEMPLATE_EDUCATION = """
        You are an expert in the field of admission consulting.
        You are provided with the following extracted parts of a long document containing information about majors, admission subject combinations, job opportunities, support policies, time and tuition fees, scholarships, ...
        and a question.
        Based on the context and give the most complete answer.
        Use the extracted documents and questions to answer first. If you don't know the answer, just say "I don't know".
        If the question is not about admission information, use your knowledge now to answer. Don't make up your own answers.
        Note: You are only allowed to use Vietnamese to answer. Answers must be polite without special characters.
        
        Question: {question}
        =========
        {context}
        =========
        Answer in Markdown:"""

EXAMPLE_QUERY_SQL = [
    {
        "input": "Điểm chuẩn ngành Công nghệ thông tin",
        "query": "SELECT diem FROM TVTS WHERE nganh = 'CÔNG NGHỆ THÔNG TIN'"
    },
    {
        "input": "Điểm chuẩn ngành CNTT CLC",
        "query": "SELECT diem FROM TVTS WHERE nganh = 'CÔNG NGHỆ THÔNG TIN (CHẤT LƯỢNG CAO)'",
    },
    {
        "input": "học phí ngành du lịch địa chất",
        "query": "SELECT hoc_phi FROM TVTS WHERE nganh = 'DU LỊCH ĐỊA CHẤT' OR ma_nganh = '7080105'",
    },
    {
        "input": "tổ hợp xét tuyển của ngành có mã 7080105",
        "query": "SELECT to_hop WHERE TVTS WHERE ma_nganh = '7080105'",
    },
    {
        "input": "Ngành kĩ thuật cơ điện tử có mã và tổ hợp xét tuyển là gì ?",
        "query": "SELECT ma_nganh, to_hop FROM TVTS WHERE nganh = 'KĨ THUẬT CƠ ĐIỆN TỬ'",
    },
    {
        "input": "Học phí của ngành CNTT và lương sau khi ra trường của ngành này",
        "query": "SELECT hoc_phi, luong_ra_truong FROM TVTS WHERE nganh = 'CÔNG NGHỆ THÔNG TIN'",
    },
    {
        "input": "26 điểm thì đỗ được ngành nào ?",
        "query": "SELECT Nganh FROM TVTS WHERE diem <= 26",
    },
    {
         "input":"Những ngành dưới 20 điểm là ngành nào ?",
         "query": "SELECT Nganh FROM TVTS WHERE diem < 20"
    },
    {
        "input": "Học phí của ngành khoa học dữ liệu là bao nhiêu ?",
        "query": "SELECT hoc_phi FROM TVTS WHERE Nganh = 'KHOA HỌC DỮ LIỆU (DATA SCIENCE)'"
    },
    {
        "input": "Điểm chuẩn ngành CNTT là bao nhiêu ?",
        "query": "SELECT diem FROM TVTS WHERE Nganh = 'CÔNG NGHỆ THÔNG TIN'"
    }
]

PROMPTING_CSV_AGENT = """
        Useful when you need to answer a question
        The questions include information such as salary, tuition, year of study, scores, training period, score, and combination of majors. 
        Not useful for answering questions unrelated to the information in the database. Use
        the entire prompt as input to the tool. For example, if the reminder is
        “How long does it take to learn IT?”, the input information must be
        "How long does it take to learn IT?".

        Note: You are only allowed to use Vietnamese to answer
        """

PROMPT_PDF_AGENT = """
        Useful in answering questions about major introductions, job opportunities, support policies and industry scholarships. 
        Not useful when answering objective questions related to information such as years of study, salary, tuition... Use
        the entire prompt as input to the tool. Use the entire prompt as
        input to the tool. For example, if the reminder is
        “How long does it take to learn IT?”, the input information must be
        “How long does it take to learn IT?”.

        Note: You are only allowed to use Vietnamese to answer
"""