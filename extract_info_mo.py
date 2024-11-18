import os
import json
from groq import Groq

def extract_info(info_type, api_key, input_file="cleaned_results.json"):
    with open(input_file, "r") as infile:
        data = infile.read()

    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Extract the following information:
                    -{info_type}
                    -give only extracted data value no other text or prompt along with it in any form not even this type
                    {data}"""
            }
        ],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    info_type = input()
    api_key = input()
    print(extract_info(info_type, api_key))
