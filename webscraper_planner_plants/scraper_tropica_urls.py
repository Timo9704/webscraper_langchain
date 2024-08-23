import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_tropica_contenturl(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div_block = soup.find('div', class_='row plant-list')
        if div_block:
            content = ""
            all_elements = div_block.find_all('a', href=True)
            for element in all_elements:
                href = element.get('href')
                if href:
                    full_url = urljoin(url, href)
                    content += full_url + "\n"
            with open("urls.txt", "w") as file:
                file.write(content)
            return content
    else:
        print(f"Failed to retrieve {url}")

# Beispielaufruf der Funktion
extract_tropica_contenturl('https://tropica.com/de/pflanzen/')
