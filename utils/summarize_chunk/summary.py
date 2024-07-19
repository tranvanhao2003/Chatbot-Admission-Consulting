from groq import Groq
import time
import os
import dotenv
from configs.load_config import LoadConfig

dotenv.load_dotenv()
APP_CFG = LoadConfig()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = APP_CFG.summarize_model
TEMPERATURE = APP_CFG.temperature
DEMILITER = APP_CFG.delimiter

def chat_GROQ_API(messages: list) -> str:
    for attempts in range(APP_CFG.max_attempts):
        try:
            client = Groq(
                api_key=GROQ_API_KEY
            )
            response = client.chat.completions.create(
                messages=messages,
                model=MODEL,
                temperature=TEMPERATURE,
                max_tokens=APP_CFG.max_token
            )
            break
        except Exception as error:
            print(error)
            time.sleep(1)
            if attempts == APP_CFG.max_attempts-1:
                return "Sever error"
            continue

    return response.choices[0].message.content

def get_chunk_summary(content: str) -> str:
    system_msg = f"""
            Tóm tắt đoạn tài liệu này 1 cách minh bạch và đầy đủ các ý quan trọng, tuy nhiên cũng không nên quá rườm rà.
            Lưu ý: bạn chỉ được sử dụng tiếng việt để trả lời.
            định dạng trả lời：{DEMILITER}<summary>"""
    
    user_msg = 'đây là danh sách tóm tắt:\n' + content
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
    ]
        
    result = chat_GROQ_API(messages)
    return result.split(DEMILITER)[-1].strip()

def get_global_summary(list_of_summaries: list) -> str:
    
    system_msg = f"""
            Bạn được cung cấp một danh sách các bản tóm tắt, mỗi bản tóm tắt sẽ tóm tắt một đoạn tài liệu theo trình tự.
            Kết hợp danh sách tóm tắt thành một bản tóm tắt chung của tài liệu.
            Lưu ý: bạn chỉ được sử dụng tiếng việt để trả lời.
            reply format：{DEMILITER}<global summary>"""
    user_msg = 'đây là danh sách tóm tắt:\n' + str(list_of_summaries)
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
    ]

    result = chat_GROQ_API(messages)
    # print(result)
    return result.split(DEMILITER)[-1].strip()
