import requests
from bs4 import BeautifulSoup
import json
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt


def visualisation(data):
    if not data:
        print("No data to visualize.")
        return

    authors = [quote['author'] for quote in data]
    author_counts = pd.Series(authors).value_counts()

    plt.figure(figsize=(10, 6))
    sb.barplot(x=author_counts.index, y=author_counts.values)
    plt.xlabel("Author")
    plt.ylabel("Frequency")
    plt.title("Author Quote Frequency")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def matchQuotes(extracted_data, quotes_data):
    matched_quotes = []
    extracted_ids = {int(id_str) for id_str in extracted_data if id_str.isdigit()}

    for quote in quotes_data.get('quotes', []):
        if quote.get('id') in extracted_ids:
            matched_quotes.append(quote)

    matched_quotes.sort(key=lambda x: x.get('id', 0))
    visualisation(matched_quotes)
    file_name = "quotes.json"
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(matched_quotes, f, ensure_ascii=False, indent=4)
    print(f"Filtered and sorted quotes have been successfully saved to {file_name}")


def getQuotes():
    url = "https://dummyjson.com/quotes?limit=1000"
    response = requests.get(url)
    response.raise_for_status()
    quotes_data = response.json()
    return quotes_data


def main(AM):
    url = 'https://tma111.netlify.app/.netlify/functions/generate?id=' + AM

    response = requests.get(url)

    if response.status_code == 200:
        print("Successfully retrieved the webpage.")
        soup = BeautifulSoup(response.text, 'html.parser')
        td_elements = soup.find_all("td")
        extracted_data = []
        for td in td_elements:
            if any(char.isdigit() for char in td.text):
                clean_text = td.text.replace("ID: ", "").replace("{", "").replace("}", "").xreplace('"id": ', '')
                extracted_data.append(clean_text.strip())
        print(extracted_data)
        quotes_data = getQuotes()
        matchQuotes(extracted_data, quotes_data)
        return extracted_data
    else:
        print("Failed to retrieve the webpage.")
        return None


main("p25009")
