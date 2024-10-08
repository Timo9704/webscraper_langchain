#This class was generated using GitHub CoPilot
import requests
from bs4 import BeautifulSoup


def extract_olibetta_content(url):
    response = requests.get(url)
    print(response.text)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = ""
        title = soup.find('div', class_='p-title').get_text(" ", strip=True) if soup.find('div',class_='p-title') else 'N/A'
        content += f"Title: {title}\n"
        original_price = soup.find('span', class_='p-price__instead').get_text(" ", strip=True) if soup.find('span',class_='p-price__instead') else 'N/A'
        content += f"Original Price: {original_price}\n"
        summary_items = soup.find('div', class_='p-summary')
        summary = summary_items.get_text(" ", strip=True) if summary_items else 'N/A'
        content += f"Summary: {summary}\n"
        details = soup.find('div', class_='p-details').get_text(" ", strip=True) if soup.find('div',class_='p-details') else 'N/A'
        content += f"Details: {details}\n"

        return content
    else:
        print(f"Failed to retrieve {url}")
        return None
