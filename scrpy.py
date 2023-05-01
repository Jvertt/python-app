import sys
import requests
import re
import json
import html2text
from typing import List, Dict
from bs4 import BeautifulSoup
from typing import List
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from concurrent.futures import ThreadPoolExecutor
from newspaper import Article

interest = "computer science"

ORGANIZATIONS = [
    # Stocks
    ["Stocks", "MarketWatch", "https://www.marketwatch.com/"],
    ["Stocks", "Seeking Alpha", "https://seekingalpha.com/"],
    ["Stocks", "Investopedia", "https://www.investopedia.com/"],

    # US Laws
    ["US Laws", "SCOTUSblog", "https://www.scotusblog.com/"],
    ["US Laws", "National Law Review", "https://www.natlawreview.com/"],
    ["US Laws", "Above the Law", "https://abovethelaw.com/"],

    # Companies
    ["Companies", "TechCrunch", "https://techcrunch.com/"],
    ["Companies", "VentureBeat", "https://venturebeat.com/"],
    ["Companies", "GeekWire", "https://www.geekwire.com/"],
    ["Companies", "Gigaom", "https://gigaom.com/"],

    # News
    ["News", "The Intercept", "https://theintercept.com/"],
    ["News", "Reason", "https://reason.com/"],
    ["News", "ProPublica", "https://www.propublica.org/"],
    ["News", "The Nation", "https://www.thenation.com/"],
]

tokenizer = T5Tokenizer.from_pretrained('t5-large')  # Use the smaller t5-small model
model = T5ForConditionalGeneration.from_pretrained('t5-large')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Use GPU if available
model.to(device)

def summarize_text(text_input: str, interest: str, category: str, max_length: int = 150, num_beams: int = 2) -> str:
    tokenized_input = tokenizer.encode(f"summarize: {interest} - {category}: " + text_input, return_tensors='pt', max_length=512, truncation=True)
    tokenized_input = tokenized_input.to(device)  # Move input to GPU if available
    outputs = model.generate(tokenized_input, max_length=max_length, num_beams=num_beams, early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary

def rank_url(url, interest, tokenizer, model):
    input_sequence = f"Rate the relevance of the webpage with the url '{url}' to the interest '{interest}' on a scale of 1 to 10."
    input_ids = tokenizer.encode(input_sequence, return_tensors='pt')
    outputs = model.generate(input_ids=input_ids, max_length=50, do_sample=True)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    score = re.findall(r'\d+', generated_text)
    return int(score[0]) if score else 0

def rank_urls(interest: str, urls: List[str]) -> List[str]:
    tokenizer = T5Tokenizer.from_pretrained('t5-base')
    model = T5ForConditionalGeneration.from_pretrained('t5-base')

    with ThreadPoolExecutor() as executor:
        ranked_urls = sorted(urls, key=lambda x: executor.submit(rank_url, x, interest, tokenizer, model).result(), reverse=True)

    return ranked_urls

def scrape_urls(interest: str, base_url: str, max_urls_per_company: int, download_timeout: int) -> List[dict]:
    scraped_data = []
    urls_scraped_count = 0

    try:
        response = requests.get(base_url, timeout=download_timeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        # Removed the filter_scraped_urls function call
        unfiltered_links = [link.get('href') for link in links if link.get('href') and link.get('href').startswith('http')]
        for i, link_url in enumerate(unfiltered_links):
            if urls_scraped_count >= max_urls_per_company:
                break

            if link_url and link_url.startswith('http'):
                try:
                    print(f"[{i + 1}] Downloading {link_url}...")
                    article = Article(link_url)
                    article.download()
                    article.parse()
                    article_text = article.text
                    urls_scraped_count += 1
                    if urls_scraped_count >= max_urls_per_company:
                        break

                    scraped_data.append({
                        'url': link_url,
                        'content': article_text
                    })

                except requests.exceptions.Timeout:
                    print(f"Timeout downloading {link_url}")
                except Exception as e:
                    print(f"Error downloading {link_url}: {e}")

        print(f"Scraped {urls_scraped_count} URLs")

    except requests.exceptions.Timeout:
        print(f"Timeout downloading {base_url}")
    except Exception as e:
        print(f"Error downloading {base_url}: {e}")

    return scraped_data

def scrape_and_process(organizations: List[List[str]], interest: str, max_urls: int, download_timeout: int, scrape_timeout: int) -> Dict[str, str]:
    print("Entering scrape_and_process...")
    scraped_urls = {}
    category_contents = {}

    with ThreadPoolExecutor() as executor:
                futures = []
                for organization in organizations:
                    category, news_organization, base_url = organization
                    print(f"Scraping {news_organization}...")
                    futures.append(executor.submit(scrape_urls, interest, base_url, max_urls, download_timeout))

                for organization, future in zip(organizations, futures):
                    category, news_organization, _ = organization
                    scraped_data = future.result()
                    ranked_data = rank_urls(interest, [data['url'] for data in scraped_data])
                    scraped_data = sorted(scraped_data, key=lambda x: ranked_data.index(x['url']))
                    scraped_data = scraped_data[:max_urls]

                    for data in scraped_data:
                        data['category'] = category
                        if category not in category_contents:
                            category_contents[category] = ''
                        category_contents[category] += '\n' + data['content']

    category_summaries = {}  # Dictionary to store summaries for each category

    for category, content in category_contents.items():
        category_summary = summarize_text(content, interest, category)
        category_summaries[category] = category_summary  # Save the summary as a variable in the dictionary
        print(f"Category: {category}")
        print(f"Summary: {category_summary}")
        print("_____________________________________")

    print("Exiting scrape_and_process...")
    return category_summaries

if __name__ == "__main__":
    with open("user_profile_data.json") as f:
        user_profile_data = json.load(f)
        # Get the interest from the user profile data
        interest = user_profile_data["interest"]
    print(f"Interest: {interest}")
    scraped_data = scrape_and_process(ORGANIZATIONS, interest, 15, 5, 15)  # Change 50 to 10

   
