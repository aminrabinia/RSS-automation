import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def call_openai_api(messages, 
                    model= "gpt-3.5-turbo", 
                    temperature=0.0, 
                    max_tokens=4000):
    try:
        response = client.chat.completions.create(model=model,
                                                messages=messages,
                                                temperature=temperature, # this is the degree of randomness of the model's output
                                                max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
                                                )
        # print("API call successful for: ", messages[1]['content'][:20])
        return response.choices[0].message.content
    
    except Exception as e:  # to be improved to handle any possible errors such as service overload
        print("Network error:", e)
        return "Sorry, there is a technical issue with the LLM API..."

def process_user_message(input_prompt):
    delimiter = "```"
    messages = [
        {'role': 'system', 'content': """
            You are a helpful job search assistant on UpWork. Go through the user content that is collected via RSS, \
         and rewrite the job summary to remove any html tags and turn it into plain text. \
         Then draft a personalized message with the details from the summary and the following format:\
         Hi, Address the problem or painpoint that needs to be solved from this job posting. \
         Then introduce me as AI expert with 5+ years of helping clients with that problem. \
         Then have a call to action for a 10 min zoom call. And sign --Amin \
         Make sure the message sounds like Alex Hormozi style. \
         Put the cleaned up job summary at the end for my information as well. 
        """},
        {'role': 'user', 'content': f"{delimiter}{input_prompt}{delimiter}"},
    ]
    api_response = call_openai_api(messages=messages, ) 
    return api_response 
    

# input_llm="hi are you there?"
# print(process_user_message(input_llm))
