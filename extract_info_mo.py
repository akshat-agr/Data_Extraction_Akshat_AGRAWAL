import os
import json
from groq import Groq

def extract_info(entity, info_type, api_key, input_file="cleaned_results.json"):
    with open(input_file, "r") as infile:
        data = infile.read()

    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Extract the following information for the entity '{entity}':
                    - {info_type}
                    - Provide only the extracted data value, no other text or prompts.
                    - Do not include any sentences like "here is the data"; just return the extracted value.
                    here is the the data to refer:
                    {data}"""
            }
        ],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    entity = input("Enter entity: ")
    info_type = input("Enter info type: ")
    api_key = input("Enter API key: ")
    print(extract_info(entity, info_type, api_key))
