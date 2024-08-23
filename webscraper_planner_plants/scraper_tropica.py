import requests
from bs4 import BeautifulSoup


def extract_tropica_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('div', class_='small-8 large-7 columns plantname')
        content = ""
        if name:
            all_elements = name.find_all(recursive=True)
            for element in all_elements:
                if element.name == 'h1':
                    content += "Pflanzenart:" + element.get_text() + "\n"
        div_block = soup.find('div', class_='small-12 medium-4 columns rightpane')
        if div_block:
            all_elements = div_block.find_all(recursive=True)
            for element in all_elements:
                if element.name == 'p':
                    content += element.get_text() + "\n"
            content += "Pflanzeninformationen" + str(extract_plant_details(response.text))
            return content
    else:
        print(f"Failed to retrieve {url}")


def extract_plant_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='specficationTable')
    plant_details = {}

    # Extracting data from the rows
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:  # Ensure the row has at least one data cell
            key = row.find('th').text.strip().replace(":", "")
            value = cells[0].text.strip()
            plant_details[key] = value

            # Checking for help text in the subsequent hidden row
            if 'helptextid' in cells[1].attrs:
                helptext_id = cells[1].find('a')['helptextid']
                help_row = soup.find('tr', id=helptext_id)
                if help_row:
                    plant_details[key + ' Help'] = help_row.find('td').text.strip()
    return plant_details

