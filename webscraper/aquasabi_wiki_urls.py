#This class was generated using GitHub CoPilot
import requests
from bs4 import BeautifulSoup

def extract_urls(url, output_file):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    target_div = soup.find('div', class_='col-12 col-lg-9 aqua-wiki-content')
    if not target_div:
        print("Das spezifische Div wurde nicht gefunden.")
        return

    links = target_div.find_all('a', href=True)
    urls = [link['href'] for link in links]

    with open(output_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')

    print(f"URLs wurden in {output_file} gespeichert.")

url = 'https://www.aquasabi.de/aquascaping-wiki'
output_file = 'sources/aquasabi_urls.txt'

if __name__ == '__main__':
    file_path = './sources/'
    extract_urls(url, output_file)