import json
import re

# Load the JSON file
with open('binance_article_titles.json', 'r') as file:
    data = json.load(file)

results = []

for sentence in data:
    tickers = set(re.findall(r'\b[A-Z]+\b', sentence))  
    if tickers: 
        result_entry = {"news": sentence}
        result_entry["tickers"] = list(tickers)
        results.append(result_entry)

for result in results:
    result["tickers"] = list(set(result["tickers"]))

with open('extracted_tickers.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

print("Extraction complete. Results saved to 'extracted_tickers.json'.")  
