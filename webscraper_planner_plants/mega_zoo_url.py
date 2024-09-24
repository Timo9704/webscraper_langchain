#This class was generated using GitHub CoPilot
import requests
from bs4 import BeautifulSoup

url = 'https://www.megazoo-shop.de/suesswasser/aquarien/glasbecken/#products'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    product_boxes = soup.find_all(class_='productbox-images list-gallery')
    urls = []

    for box in product_boxes:
        links = box.find_all('a', href=True)
        for link in links:
            urls.append(link['href'])

    with open('urls.txt', 'w') as file:
        for url in urls:
            file.write(url + '\n')

    print(f'{len(urls)} URLs wurden erfolgreich in die Datei "urls.txt" geschrieben.')
else:
    print(f'Fehler: Die Seite konnte nicht aufgerufen werden. Statuscode: {response.status_code}')
