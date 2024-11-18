import json
from serpapi.google_search import GoogleSearch
import pandas as pd

def fetch_search_results(entity, info, api_key):
    params = {
        "engine": "google",
        "q": f"{entity} {info}",
        "api_key": api_key
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    
    with open("search_results.json", "w") as outfile:
        json.dump(organic_results, outfile)

if __name__ == "__main__":
    file_path = input("Enter file path: ")
    df = pd.read_csv(file_path)
    info = input("Enter info you want: ")
    api_key = input("Enter API key: ")
    
    for value in df['entity']:
        fetch_search_results(value, info, api_key)
