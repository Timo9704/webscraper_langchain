import requests
from bs4 import BeautifulSoup

# URL der Ziel-Webseite
url = 'https://www.megazoo-shop.de/suesswasser/aquarien/glasbecken/#products'

# HTTP-GET Anfrage an die Webseite
response = requests.get(url)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # Webseite parsen
    soup = BeautifulSoup(response.content, 'html.parser')

    # Alle Links unter den Elementen mit den Klassen 'productbox-images list-gallery' finden
    product_boxes = soup.find_all(class_='productbox-images list-gallery')

    # Liste, um die URLs zu speichern
    urls = []

    # Durch die gefundenen Elemente iterieren und die Links extrahieren
    for box in product_boxes:
        links = box.find_all('a', href=True)
        for link in links:
            # URL zur Liste hinzufügen
            urls.append(link['href'])

    # URLs in die Datei 'urls.txt' schreiben
    with open('urls.txt', 'w') as file:
        for url in urls:
            file.write(url + '\n')

    print(f'{len(urls)} URLs wurden erfolgreich in die Datei "urls.txt" geschrieben.')
else:
    print(f'Fehler: Die Seite konnte nicht aufgerufen werden. Statuscode: {response.status_code}')
