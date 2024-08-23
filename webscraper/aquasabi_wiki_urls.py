import requests
from bs4 import BeautifulSoup

def extract_urls(url, output_file):
    # Webseite abrufen
    response = requests.get(url)
    response.raise_for_status()  # stellt sicher, dass die Anfrage erfolgreich war

    # HTML-Inhalt mit BeautifulSoup analysieren
    soup = BeautifulSoup(response.text, 'html.parser')

    # Spezifisches Div finden
    target_div = soup.find('div', class_='col-12 col-lg-9 aqua-wiki-content')
    if not target_div:
        print("Das spezifische Div wurde nicht gefunden.")
        return

    # Alle Links innerhalb des Divs extrahieren
    links = target_div.find_all('a', href=True)
    urls = [link['href'] for link in links]

    # URLs in eine Datei schreiben
    with open(output_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')

    print(f"URLs wurden in {output_file} gespeichert.")

# URL der Webseite und der Pfad der Ausgabedatei
url = 'https://www.aquasabi.de/aquascaping-wiki'  # Setze hier die URL der gewünschten Webseite
output_file = 'sources/aquasabi_urls.txt'

if __name__ == '__main__':
    # Pfad zur Datei mit den URLs
    file_path = './sources/'
    # Funktion aufrufen
    extract_urls(url, output_file)