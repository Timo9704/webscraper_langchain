import requests
from bs4 import BeautifulSoup


def extract_drta_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        fish_details = {}

        # Extracting data from the rows
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:  # Ensure the row has exactly two cells
                key = cells[0].text.strip().replace(":", "")
                value = cells[1].text.strip()
                fish_details[key] = value
        return str(fish_details)
    else:
        print(f"Failed to retrieve {url}")
