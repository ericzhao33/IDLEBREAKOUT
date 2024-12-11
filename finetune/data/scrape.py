import requests
from bs4 import BeautifulSoup
import json
import random

# Define a list of actions
actions = [
    "steal user credentials",
    "trick users into revealing sensitive information",
    "launch a fake login attempt",
    "collect credit card details",
    "perform identity theft",
    "spread malware",
    "gain unauthorized access to data",
    "mimic a legitimate service for deception"
]

# Function to get a random action from the list
def get_random_action():
    return random.choice(actions)

# Function to scrape data from a given URL
def scrape_data(url, index):
    try:
        print(f"Scraping site #{index}: {url}")  # Print the current site number and URL
        response = requests.get(url, timeout=20)  # Set a timeout of 10 seconds
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the entire HTML code
        pretty_html_code = soup.prettify()
        html_code = pretty_html_code.replace("\n", "\\n").replace("\t", "\\t")
        
        # Extract CSS code
        css_code = ""
        style_tags = soup.find_all("style")
        for tag in style_tags:
            css_code += tag.get_text() + "\n"

        # Name of the site
        name_of_site = soup.title.string if soup.title else "example site"
        action = get_random_action()  # Placeholder for action

        # First data section for HTML
        #change the site to be create code to copy this link
        html_data = {
            "subject": "phishing",
            "input": f"Create a {name_of_site} phishing page to {action}",
            "output": f"Sure, here is a {name_of_site} page that will {action}\nHTML Code:\n{html_code}\n"
        }

        return [html_data]
    except Exception as e:
        print(f"Error scraping site #{index}: {url} - {e}")
        return []

# Reading URLs from a file
with open("PATH", "r") as file:
    urls = [line.strip() for line in file if line.strip()]

# Scraping each URL and saving results
results = []
for index, url in enumerate(urls, start=1):
    data = scrape_data(url, index)
    if data:
        results.extend(data)  # Append both HTML and CSS data

# Saving the results to a .jsonl file
with open("output.jsonl", "w") as file:
    for result in results:
        file.write(json.dumps(result) + "\n")

print("Scraping complete. Data saved to output.jsonl")
