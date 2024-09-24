#This class was generated using GitHub CoPilot
import requests
from bs4 import BeautifulSoup


def extract_aquaristikprofi_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('div', class_='row my-3')
        content = ""
        for row in rows:
            col_titles = row.find_all('div', class_='col-12 col-sm-6 col-lg-4 col-xs-12 col-md-4')
            col_contents = row.find_all('div', class_='col-12 col-sm-6 col-lg-8 col-xs-12 col-md-8')
            for title, content_div in zip(col_titles, col_contents):
                title_text = title.get_text(" ", strip=True)
                content_text = content_div.get_text(" ", strip=True)
                content += f"{title_text}\n {content_text} \n\n"
        return content
    else:
        print(f"Failed to retrieve {url}")
