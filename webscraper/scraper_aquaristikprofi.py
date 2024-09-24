#This class was generated using GitHub CoPilot
import requests
from bs4 import BeautifulSoup


def extract_aquaristikprofi_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div_block = soup.find('div', id_='page-content')
        if div_block:
            content = ""
            for element in div_block.children:
                if element.name == 'p':
                    content += element.get_text() + "\n"
                elif element.name == 'ul':
                    for li in element.find_all('li'):
                        content += li.get_text() + "\n"
            return content
    else:
        print(f"Failed to retrieve {url}")
