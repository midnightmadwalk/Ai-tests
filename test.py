import requests
import json

#check baki
base_url = "https://www.binance.com/bapi/composite/v1/public/cms/article/catalog/list/query"
catalog_id = "48"
page_size = 50
total_pages = 31  

titles = []

for page_no in range(1, total_pages + 1):
    response = requests.get(base_url, params={
        "catalogId": catalog_id,
        "pageNo": page_no,
        "pageSize": page_size
    })
    if response.status_code == 200:
        data = response.json()
        articles = data.get('data', {}).get('articles', [])
        titles.extend(article.get('title') for article in articles if article.get('title'))
    else:
        print(f"Failed to fetch page {page_no}: {response.status_code}")

with open('binance_article_titles.json', 'w') as file:
    json.dump(titles, file, indent=4)

print("Titles successfully saved to binance_article_titles.json")
