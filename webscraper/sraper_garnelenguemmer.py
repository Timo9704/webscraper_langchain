#This class was generated using GitHub CoPilot
import requests
from bs4 import BeautifulSoup


# Funktion zum Extrahieren des gewünschten Inhalts
def extract_garnelenguemmer_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div_block = soup.find('div', class_='blog--detail-description block')
        if div_block:
            content = ""
            all_elements = div_block.find_all(recursive=False)
            for element in all_elements:
                if element.find(class_='box--content is--rounded'):
                    continue
                if element.name == 'p':
                    content += element.get_text() + "\n"
                elif element.name == 'ul':
                    for li in element.find_all('li'):
                        content += li.get_text() + "\n"
            return content
    else:
        print(f"Failed to retrieve {url}")
