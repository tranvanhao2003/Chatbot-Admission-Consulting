from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
import os
from langchain_groq import ChatGroq
import requests
# URL of the API endpoint
url = "https://api.groq.com/openai/v1/models"

# List of API keys to try
api_keys = [
    "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",
    "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",
    "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"
]

def try_api_keys(api_keys, url):
    groq_api_key = None  # Initialize the variable to store the working API key
    for api_key in api_keys:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            # Check the HTTP status code of the response
            if response.status_code == 200:
                print("API key is working:", api_key)
                groq_api_key = api_key  # Assign the working API key
                break  # Stop trying if a working key is found
            elif response.status_code == 401:
                print("API key is invalid or expired:", api_key)
            else:
                print(f"API returned status code {response.status_code} for key: {api_key}")
        except requests.exceptions.RequestException as e:
            print(f"API request failed with key {api_key}: {e}")

    return groq_api_key

# Call the function with the list of API keys
groq_api_key = try_api_keys(api_keys, url)
#-----------------------------------------------------------------------------------------------------------
os.environ['GROQ_API_KEY'] = groq_api_key
llm = ChatGroq(model="llama3-8b-8192",temperature =0)

def spelling_correct_sentences(text_input):
    examples =  [
        {
            "input_text":"toi muon ban gioi tthieu ve nganh cong nghe thong tin",
            "command":"tôi muốn bạn giới thiệu về ngành công nghệ thông tin"
        },
        {
            "input_text":"nghành kĩ thaut o to học trong bao lau",
            "command":"ngành kỹ thuật ô tô học trong bao lâu"
        },
        {
            "input_text":"tgian và hphi ngành khoa hoc du lieu",
            "command":"Thời gian và học phí ngành khoa học dữ liệu"
        },
        {
            "input_text":"Co hoi viec lam cho nganh du lịch dia chat",
            "command":"Cơ hội việc làm cho ngành du lịch địa chất."
        },
        {
            "input_text":"to hop xet tuyen nganh ki thaut o to",
            "command":"Tổ hợp xét tuyển ngành kỹ thuật ô tô"
        }]
    example_formatter_template = """
        input text from user: {input_text}

        correct input and insert command below:
        command: {command}
    """
    example_prompt = PromptTemplate(
        input_variables=["input_text", "command"],
        template=example_formatter_template,
    )
    few_shot_prompt = FewShotPromptTemplate(
        # These are the examples we want to insert into the prompt.
        examples=examples,
        # This is how we want to format the examples when we insert them into the prompt.
        example_prompt=example_prompt,
        # The prefix is some text that goes before the examples in the prompt.
        prefix="Please correct the following sentence for correct spelling and lowercase. Return the correctly spelled sentence.",
        # The suffix is some text that goes after the examples in the prompt.
        suffix="input command from user: {input_text}\ninformation corrected for spelling from the above command",
        # The input variables are the variables that the overall prompt expects.
        input_variables=["input_text"],
        # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
        example_separator="\n\n",
    )
    # Print the formatted prompt for debugging purposes (optional)
    chain = LLMChain(llm=llm, prompt=few_shot_prompt)

    result = chain.run(input_text=text_input)
    
    return result.lower()

# for i in range(1, 50):

# x = spelling_correct_sentences('toi muon xem ma nganh cong nghe thong tin')
# print(x)