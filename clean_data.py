import re
import json

def clean_json_data(input_file, output_file):
    with open(input_file, "r") as infile:
        data = infile.read()

    cleaned_data = re.sub(r'"(link|redirect_link|displayed_link|favicon)":\s*"[^"]+",?', '', data)
    
    
    with open(output_file, "w") as outfile:
        outfile.write(cleaned_data)

if __name__ == "__main__":
    clean_json_data("search_results.json", "cleaned_results.json")
